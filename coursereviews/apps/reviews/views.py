from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reviews.models import Review, Professor, Course, ProfCourse
from reviews.forms import ReviewForm
from reviews.decorators import quota_required
from reviews.utils import Review_Aggregator
from haystack.query import SearchQuerySet
from haystack.inputs import Clean

from operator import __or__

@login_required
def quota(request):
  return TemplateResponse(request, 'reviews/quota.html')

@quota_required
def browse(request):
    recent_reviews = Review.objects.select_related().order_by('-date')[:10]
    profs = Professor.objects.all()[:10]
    courses = Course.objects.all()[:10]
    return TemplateResponse(request, 'reviews/browse.html', { 'recent_reviews': recent_reviews, 'profs': profs, 'courses': courses })

@quota_required
def browseProfs(request):
    pass 

@quota_required
def browseCourses(request):
    pass

def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    # Get all Prof_Courses objects for a course
    prof_courses = course.prof_courses.all().select_related()

    # Gather all the reviews for a course
    reviews = reduce(__or__, 
                     map(lambda pc: pc.reviews \
                                      .all()   \
                                      .values('components',
                                              'again',
                                              'hours',
                                              'grasp',
                                              'value',
                                              'why_take',
                                              'comment'), prof_courses))

    # Aggregate the values
    aggregator = Review_Aggregator(reviews)
    stats = aggregator.aggregate()

    return TemplateResponse(request, 
                            'reviews/review_detail.html', 
                            { 'course': course, 
                              'prof_courses': prof_courses,
                              'data': stats,
                              'type': 'course' })

def prof_detail(request, prof_slug):
    professor = get_object_or_404(Professor, slug=prof_slug)

    # Get all Prof_Courses objects for a professor
    prof_courses = professor.prof_courses.all().select_related()

    reviews = reduce(__or__,
                     map(lambda pc: pc.reviews \
                                      .all()   \
                                      .values('another',
                                              'prof_lecturing',
                                              'prof_leading',
                                              'prof_help',
                                              'prof_feedback',
                                              'comment'), prof_courses))

    aggregator = Review_Aggregator(reviews)
    stats = aggregator.aggregate()
    return TemplateResponse(request, 
                            'reviews/review_detail.html', 
                            { 'prof': professor, 
                              'prof_courses': prof_courses,
                              'data': stats,
                              'type': 'prof' })

def prof_course_detail(request, course_slug, prof_slug):
    prof_course = get_object_or_404(ProfCourse.objects.select_related(), 
                                    course__slug__exact=course_slug, 
                                    prof__slug__exact=prof_slug)

    # Get all reviews for the prof_courses
    reviews = prof_course.reviews.all().values()

    aggregator = Review_Aggregator(reviews)
    stats = aggregator.aggregate()

    return TemplateResponse(request,
                            'reviews/review_detail.html',
                            { 'prof_course': prof_course,
                              'data': stats,
                              'type': 'prof_course'})

@login_required
def create(request):
  if request.method == "GET":
    form = ReviewForm(initial={'hours': 0})
    return TemplateResponse(request, 'reviews/edit.html', {'form': form})
  elif request.method == "POST":
    review = Review(user=request.user)
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
      form.save()
      profile = request.user.get_profile()
      profile.quota -= 1
      profile.save()
      return redirect('index')
    else:
      return TemplateResponse(request, 'reviews/edit.html', {'form': form})

def detail(request, review_id, edit=False):
  review = get_object_or_404(Review.objects.select_related(), id=review_id)
  if edit == True:
    if request.user != review.user:
      return HttpResponse(status=404)
    if request.method == "GET":
      form = ReviewForm(instance=review)
      return TemplateResponse(request, 'reviews/edit.html', {'form': form})
    elif request.method == "POST":
      form = ReviewForm(request.POST, instance=review)
      if form.is_valid():
        form.save()
        return redirect(review)
      else:
        return TemplateResponse(request, 'reviews/edit.html', {'form': form})
  else:
    return TemplateResponse(request, 'reviews/view.html', {'review': review})

@require_GET
def delete(request, review_id):
  review = get_object_or_404(Review, id=review_id)
  if request.user == review.user:
    review.delete()
    return redirect('/')
  return HttpResponse(status=403)

@require_GET
def search(request):
  query = request.GET.get("q", "")

  # Check if result exactly matches a professor
  try:
    result = Professor.objects.get(lookup__iexact=query)
    return redirect('prof_detail', result.slug)
  except Professor.DoesNotExist:
    pass

  # Check if a result exactly matches a course
  try:
    result = Course.objects.get(lookup__iexact=query)
    return redirect('course_detail', result.slug)
  except Course.DoesNotExist:
    pass

  # Perform a search using Haystack
  course_results = SearchQuerySet().models(Course).filter(content=Clean(query))
  professor_results = SearchQuerySet().models(Professor).filter(content=Clean(query))

  results_count = len(course_results) + len(professor_results)

  ctx_dict = {'count': results_count,
              'courses': course_results,
              'professors': professor_results,
              'query': query}
  return TemplateResponse(request, 'reviews/search_results.html', ctx_dict)
