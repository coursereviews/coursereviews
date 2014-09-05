from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.db.models import F

from reviews.models import (Review,
                            Professor,
                            Course,
                            ProfCourse,
                            Department)
from reviews.forms import ReviewForm, FlagForm
from reviews.decorators import quota_required, no_professor_access
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

    # Get professor association, None if student
    user_professor = request.user.get_profile().professor_assoc

    if user_professor:
        prof_courses = course.prof_courses.filter(prof=user_professor).select_related()
    else:
        # Get all Prof_Courses objects for a course
        prof_courses = course.prof_courses.all().select_related()

    # If this is not a professor account
    if user_professor == None or user_professor in [pc.prof for pc in prof_courses]:

        flag_form = FlagForm()

        # Gather all the reviews for a course
        reviews = sorted(reduce(__or__, map(lambda pc: pc.reviews.all().exclude(flagged=True), prof_courses)),
                         key=attrgetter('vote_difference'), reverse=True)

        has_comments = any([review.comment for review in reviews])

        return TemplateResponse(request, 'reviews/review_detail.html',
                                { 'course': course,
                                  'prof_courses': prof_courses,
                                  'reviews': reviews,
                                  'flag_form': flag_form,
                                  'has_comments': has_comments,
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

        flag_form = FlagForm()

        try:
            reviews = sorted(reduce(__or__, map(lambda pc: pc.reviews.all().exclude(flagged=True), prof_courses)),
                             key=attrgetter('vote_difference'), reverse=True)
        except TypeError:
            reviews = []

        has_comments = any([review.comment for review in reviews])

        return TemplateResponse(request, 'reviews/review_detail.html',
                                { 'prof': professor,
                                  'prof_courses': prof_courses,
                                  'reviews': reviews,
                                  'flag_form': flag_form,
                                  'has_comments': has_comments,
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

        flag_form = FlagForm()

        # Get all reviews for the prof_courses
        reviews = sorted(prof_course.reviews.all().exclude(flagged=True),
                         key=attrgetter('vote_difference'), reverse=True)

        has_comments = any([review.comment for review in reviews])

        return TemplateResponse(request,
                                'reviews/review_detail.html',
                                { 'prof_course': prof_course,
                                  'reviews': reviews,
                                  'flag_form': flag_form,
                                  'has_comments': has_comments,
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
        if form.is_valid():
            form.save()
            profile = request.user.get_profile()
            profile.semester_reviews = F('semester_reviews') + 1
            profile.total_reviews = F('total_reviews') + 1
            profile.save()

            return redirect('prof_course_detail', course_slug=review.prof_course.course.slug, prof_slug=review.prof_course.prof.slug)
        else:
            return TemplateResponse(request, 'reviews/edit.html', {'form': form})

@login_required
@no_professor_access
def edit(request, review_id):
    review = get_object_or_404(Review.objects.select_related(), id=review_id)

    # Cannot view an individual review of another user
    if request.user != review.user or not review.editable:
        raise Http404

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
    except (Professor.DoesNotExist, Professor.MultipleObjectsReturned):
        pass

    # Check if a result exactly matches a course
    try:
        result = Course.objects.get(lookup__iexact=query)
        return redirect('course_detail', result.slug)
    except (Course.DoesNotExist, Course.MultipleObjectsReturned):
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


@require_GET
def profile(request):
    review_qs = request.user.reviews.all()
    review_qs = review_qs.prefetch_related('prof_course__course', 'prof_course__prof')
    return TemplateResponse(request, 'reviews/profile.html', {
        'reviews': review_qs
    })

