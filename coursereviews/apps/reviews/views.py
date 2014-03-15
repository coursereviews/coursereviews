from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from reviews.models import Review, Professor, Course, ProfCourse
from reviews.forms import ReviewForm
from reviews.decorators import quota_required
from reviews.utils import Review_Aggregator, user_vote_type
from reviews.serializers import CommentSerializer

from haystack.query import SearchQuerySet
from haystack.inputs import Clean
from rest_framework.response import Response

from operator import __or__
import json

@login_required
def quota(request):
    return TemplateResponse(request, 'reviews/quota.html')

@quota_required
def browse(request):
    profs = Professor.objects.all()[:10]
    courses = Course.objects.all()[:10]
    return TemplateResponse(request, 'reviews/browse.html', { 'profs': profs, 'courses': courses })

@quota_required
def browseProfs(request):
    pass 

@quota_required
def browseCourses(request):
    pass

@login_required
@quota_required
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
    stats = aggregator.aggregate(as_dict=True)

    try:
      comments = stats['comments']
    except KeyError:
      comments = []

    return TemplateResponse(request, 
                            'reviews/review_detail.html', 
                            { 'course': course, 
                              'prof_courses': prof_courses,
                              'comments': comments,
                              'data': json.dumps(stats),
                              'type': 'course' })

def prof_detail(request, prof_slug):
    professor = get_object_or_404(Professor.objects.select_related(), slug=prof_slug)

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
                                              'comment',
                                              'prof_course'), prof_courses))

    aggregator = Review_Aggregator(reviews, attach_comment_slug=True)
    stats = aggregator.aggregate(as_dict=True)

    print stats

    try:
      comments = stats['comments']
    except KeyError:
      comments = []

    return TemplateResponse(request, 
                            'reviews/review_detail.html', 
                            { 'prof': professor, 
                              'prof_courses': prof_courses,
                              'comments': comments,
                              'data': json.dumps(stats),
                              'type': 'prof' })

def prof_course_detail(request, course_slug, prof_slug):
    prof_course = get_object_or_404(ProfCourse.objects.select_related(), 
                                    course__slug__exact=course_slug, 
                                    prof__slug__exact=prof_slug)

    # Get all reviews for the prof_courses
    reviews = prof_course.reviews.all().values()

    aggregator = Review_Aggregator(reviews)
    stats = aggregator.aggregate(as_dict=True)

    try:
      comments = stats['comments']
    except KeyError:
      comments = []

    return TemplateResponse(request,
                            'reviews/review_detail.html',
                            { 'prof_course': prof_course,
                              'comments': comments,
                              'data': json.dumps(stats),
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
            if profile.quota > 0:
                profile.quota -= 1
                profile.save()
            return redirect('index')
        else:
            return TemplateResponse(request, 'reviews/edit.html', {'form': form})

def edit(request, review_id):
    review = get_object_or_404(Review.objects.select_related(), id=review_id)

    # Cannot view an individual review of another user
    if request.user != review.user:
        return HttpResponse(status=404)

    # Show the edit page
    if request.method == "GET":
        form = ReviewForm(instance=review)
        return TemplateResponse(request, 'reviews/edit.html', {'form': form})

    # Update the review
    elif request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return TemplateResponse(request, 'reviews/edit.html', {'form': form})

    else:
        return HttpResponse(status=404)

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

    print course_results

    results_count = len(course_results) + len(professor_results)

    ctx_dict = {'count': results_count,
                'courses': course_results,
                'professors': professor_results,
                'query': query}
    return TemplateResponse(request, 'reviews/search_results.html', ctx_dict)

@require_POST
@login_required
def vote(request, review_id):
    user = request.user
    review = Review.objects.get(id=review_id)
    vote_type = request.POST.get('vote_type', None)

    if vote_type == 'up':
        if user not in review.up_votes:
            review.up_votes.add(user)

            if user in review.down_votes:
                review.down_votes.remove(user)

            serializer = CommentSerializer(review, 
                                           context={'user_vote_type': user_vote_type(request, review_id)})
            return Response(serializer.data)
        else:
            return HttpResponse(json.dumps({'error': 'User has already upvoted this comment.'}), status=400)

    elif vote_type == 'down':
        if user not in review.down_votes:
            review.down_votes.add(user)

            if user in review.up_votes:
                review.down_votes.remove(user)

            serializer = CommentSerializer(review,
                                           context={'user_vote_type': user_vote_type(request, review_id)})
            return Response(serializer.data)
        else:
            return HttpResponse(json.dumps({'error': 'User has already downvoted this comment.'}), status=400)

    else:
        return HttpResponse(status=403)
