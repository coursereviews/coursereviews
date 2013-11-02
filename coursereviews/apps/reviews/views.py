from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reviews.models import Review, Professor, Course
from reviews.forms import ReviewForm
from reviews.decorators import quota_required
from haystack.query import SearchQuerySet
from haystack.inputs import Clean

from django.core import serializers
from operator import __or__

@login_required
def quota(request):
  return TemplateResponse(request, 'reviews/quota.html')

@quota_required
def browse(request):
    profs = Professor.objects.all()[:5]
    courses = Course.objects.all()[:5]
    return TemplateResponse(request, 'reviews/browse.html', { 'profs': profs, 'courses': courses })

@quota_required
def browseProfs(request):
    pass 

@quota_required
def browseCourses(request):
    pass

def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    prof_courses = course.prof_courses.all()
    # print prof_courses
    reviews_queryset = reduce(__or__, map(lambda pc: pc.reviews.all(), prof_courses))
    print reviews_queryset
    reviews = serializers.serialize('json', reviews_queryset, use_natural_keys=True)
    print reviews
    return TemplateResponse(request, 'reviews/course_detail.html', {'course': course, 'reviews': reviews })
    # return TemplateResponse(request, 'reviews/browse.html', { 'profs': profs, 'courses': courses })

def prof_detail(request, prof_slug):
  professor = Professor.objects.get(slug=prof_slug)
  return TemplateResponse(request, 'reviews/prof_detail.html', {'professor': professor})    

@login_required
def create(request):
  if request.method == "GET":
    form = ReviewForm(initial={'hours': 0})
    return TemplateResponse(request, 'reviews/edit.html', {'form': form})
  elif request.method == "POST":
    review = Review(user=request.user)
    form = ReviewForm(request.POST, instance=review)
    print request.POST
    if form.is_valid():
      form.save()
      profile = request.user.get_profile()
      profile.quota -= 1
      profile.save()
      return redirect('index')
    else:
      print form.errors
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
      print request.POST
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
