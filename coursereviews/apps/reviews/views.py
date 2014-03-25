from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

from reviews.models import (Review,
                            Professor,
                            Course,
                            ProfCourse,
                            Department)
from reviews.forms import ReviewForm
from reviews.decorators import quota_required, no_professor_access
from reviews.utils import Review_Aggregator, user_vote_type
from reviews.serializers import CommentSerializer

from haystack.query import SearchQuerySet
from haystack.inputs import Clean
from rest_framework.response import Response

from operator import __or__, attrgetter
import json

def browse(request):
    user_professor = request.user.get_profile().professor_assoc
    if not user_professor:
        departments = Department.objects.all().order_by('name').select_related()
        profs_courses_by_dept = []

        for dept in departments:
            dept_courses = dept.courses.all()
            dept_profs = dept.professors.all()

            # We can hide professor categories with no professors in the template
            # Those professors still teach courses, they just might be in different departments
            if dept_courses:
                profs_courses_by_dept.append({ 'dept': dept, 'courses': dept_courses, 'profs': dept_profs })

        return TemplateResponse(request, 'reviews/student_browse.html', {  'profs_courses_by_dept': profs_courses_by_dept })
    else:
        courses = ProfCourse.objects.filter(prof=user_professor)
        return TemplateResponse(request, 'reviews/prof_browse.html', { 'professor': user_professor, 'courses': courses })

@login_required
@quota_required
def course_detail(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    # Get all Prof_Courses objects for a course
    prof_courses = course.prof_courses.all().select_related()

    # If this is a professor account
    user_professor = request.user.get_profile().professor_assoc
    if user_professor == None or user_professor in [pc.prof for pc in prof_courses]:

        # Gather all the reviews for a course
        reviews = sorted(reduce(__or__, map(lambda pc: pc.reviews.all(), prof_courses)),
                         key=attrgetter('vote_difference'), reverse=True)

        return TemplateResponse(request, 'reviews/review_detail.html', 
                                { 'course': course, 
                                  'prof_courses': prof_courses,
                                  'reviews': reviews,
                                  'type': 'course' })
    else:
        raise Http404


@login_required
@quota_required
def prof_detail(request, prof_slug):
    professor = get_object_or_404(Professor.objects.select_related(), slug=prof_slug)

    # Get all Prof_Courses objects for a professor
    prof_courses = professor.prof_courses.all().select_related()

    # If this is a professor account
    user_professor = request.user.get_profile().professor_assoc
    if user_professor == None or user_professor == professor:

        try:
            reviews = sorted(reduce(__or__, map(lambda pc: pc.reviews.all(), prof_courses)),
                             key=attrgetter('vote_difference'), reverse=True)
        except TypeError:
            reviews = []

        return TemplateResponse(request, 'reviews/review_detail.html', 
                                { 'prof': professor, 
                                  'prof_courses': prof_courses,
                                  'reviews': reviews,
                                  'type': 'prof' })
    else:
        raise Http404


@login_required
@quota_required
def prof_course_detail(request, course_slug, prof_slug):
    prof_course = get_object_or_404(ProfCourse.objects.select_related(), 
                                    course__slug__exact=course_slug, 
                                    prof__slug__exact=prof_slug)

    user_professor = request.user.get_profile().professor_assoc
    if user_professor == None or user_professor == prof_course.prof:

        # Get all reviews for the prof_courses
        reviews = sorted(prof_course.reviews.all(), key=attrgetter('vote_difference'), reverse=True)

        return TemplateResponse(request,
                                'reviews/review_detail.html',
                                { 'prof_course': prof_course,
                                  'reviews': reviews,
                                  'type': 'prof_course'})
    else:
        raise Http404

@login_required
@no_professor_access
def create(request):
    if request.method == "GET":
        form = ReviewForm(initial={'hours': 0})
        return TemplateResponse(request, 'reviews/edit.html', {'form': form})
    elif request.method == "POST":
        review = Review(user=request.user)
        form = ReviewForm(request.POST, instance=review)
        print form
        if form.is_valid():
            form.save()
            profile = request.user.get_profile()
            if profile.quota > 0:
                profile.quota -= 1
                profile.save()
            return redirect('index')
        else:
            return TemplateResponse(request, 'reviews/edit.html', {'form': form})

@login_required
@no_professor_access
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
