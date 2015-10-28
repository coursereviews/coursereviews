from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import (Http404,
                         HttpResponse)
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404

from reviews.models import (Review,
                            Professor,
                            Course,
                            ProfCourse,
                            Department)
from reviews.serializers import (CommentSerializer,
                                 DepartmentSerializer,
                                 CourseSerializer,
                                 ProfessorSerializer)

from reviews.utils import Review_Aggregator
from reviews.decorators import no_professor_access
from reviews.forms import FlagForm

from operator import __or__
import json

class Departments(APIView):
    def get(self, request, format=None):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)

        return Response(serializer.data)


class Courses(APIView):
    """
    An API view to retrieve all the courses for a department.
    """
    def get(self, request, format=None):
        queryset = Department.objects.all()

        department = request.GET.get('department', None)
        if not department:
            raise Http404

        dept = get_object_or_404(queryset, id=department)

        courses = Course.objects.filter(dept=dept)
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)


class Professors(APIView):
    """
    An API view to retrieve all the professors for a department.
    """
    def get(self, request, format=None):
        queryset = Department.objects.all()

        department = request.GET.get('department', None)
        if not department:
            raise Http404
            
        dept = get_object_or_404(queryset, id=department)

        professors = Professor.objects.filter(dept=dept)
        serializer = ProfessorSerializer(professors, many=True)

        return Response(serializer.data)


class Comment(APIView):
    """
    Retrieve or update flag/vote data on a comment.
    """

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        review = self.get_object(pk)
        serializer = CommentSerializer(review)
        return Response(serializer.data)

def typeahead_courses(request):
    courses = Course.objects.all()
    course_index = map(lambda course: {
        "name": course.title,
        "value": course.lookup,
        "tokens": get_course_tokens(course)
        }, courses)

    return HttpResponse(json.dumps(course_index), status=200)

def typeahead_professors(request):
    professors = Professor.objects.all()
    professor_index = map(lambda professor: {
        "name": professor.__unicode__(),
        "value": professor.lookup,
        "tokens": get_professor_tokens(professor)
        }, professors)

    return HttpResponse(json.dumps(professor_index), status=200)

@login_required
@csrf_protect
def prof_detail_stats(request, prof_slug):
    """
    Aggregated stats for the professor charts.
    """
    try:
        professor = Professor.objects.select_related().get(slug=prof_slug)
    except Professor.DoesNotExist:
        return HttpResponse(status=404)

    prof_courses = professor.prof_courses.all().select_related()

    user_professor = request.user.userprofile.professor_assoc
    if user_professor == None or user_professor == professor:

        try:
            reviews = reduce(__or__,
                             map(lambda pc: pc.reviews \
                                              .all()   \
                                              .values('another',
                                                      'prof_lecturing',
                                                      'prof_leading',
                                                      'prof_help',
                                                      'prof_feedback'), prof_courses))
        except TypeError:
            reviews = []

        aggregator = Review_Aggregator(reviews)
        stats = aggregator.aggregate()

        return HttpResponse(json.dumps(stats), status=200)
    else:
        raise HttpResponse(status=403)

@login_required
@csrf_protect
def course_detail_stats(request, course_slug):
    """
    Aggregated stats for the course charts.
    """
    try:
        course = Course.objects.select_related().get(slug=course_slug)
    except Course.DoesNotExist:
        return HttpResponse(status=404)

    # Get all Prof_Courses objects for a course
    prof_courses = course.prof_courses.all().select_related()

    # If this is a professor account
    user_professor = request.user.userprofile.professor_assoc
    if user_professor == None or user_professor in [pc.prof for pc in prof_courses]:

        # Gather all the reviews for a course
        reviews = reduce(__or__,
                         map(lambda pc: pc.reviews \
                                          .all()   \
                                          .values('components',
                                                  'again',
                                                  'hours',
                                                  'grasp',
                                                  'value',
                                                  'why_take'), prof_courses))

        # Aggregate the values
        aggregator = Review_Aggregator(reviews)
        stats = aggregator.aggregate()

        return HttpResponse(json.dumps(stats), status=200)
    else:
        return HttpResponse(status=403)

@login_required
@csrf_protect
def prof_course_detail_stats(request, course_slug, prof_slug):
    """
    Aggregated stats for the prof_course charts.
    """
    try:
        prof_course = ProfCourse.objects.select_related() \
                                .get(course__slug__exact=course_slug,
                                     prof__slug__exact=prof_slug)
    except ProfCourse.DoesNotExist:
        return HttpResponse(status=404)

    user_professor = request.user.userprofile.professor_assoc
    if user_professor == None or user_professor == prof_course.prof:

        # Get all reviews for the prof_courses
        reviews = prof_course.reviews.all().values('components', 'again',
                                                   'hours', 'another', 'grasp',
                                                   'prof_lecturing', 'prof_leading',
                                                   'prof_help', 'prof_feedback',
                                                   'value', 'why_take')

        aggregator = Review_Aggregator(reviews)
        stats = aggregator.aggregate()

        return HttpResponse(json.dumps(stats), status=200)
    else:
        return HttpResponse(404)

@login_required
@no_professor_access
@csrf_protect
@api_view(['POST',])
def vote(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return HttpResponse(status=404)

    if review.flagged:
        return HttpResponse(status=403)

    user = request.user
    vote_type = request.POST.get('vote_type', None)

    if vote_type == 'up':
        if user not in review.up_votes.all():
            review.up_votes.add(user)

            if user in review.down_votes.all():
                review.down_votes.remove(user)

            serializer = CommentSerializer(review, context={'request': request})
            return Response(serializer.data)
        else:
            return HttpResponse(json.dumps({'error': 'User has already upvoted this comment.'}), status=400)

    elif vote_type == 'down':
        if user not in review.down_votes.all():
            review.down_votes.add(user)

            if user in review.up_votes.all():
                review.up_votes.remove(user)

            serializer = CommentSerializer(review, context={'request': request})
            return Response(serializer.data)
        else:
            return HttpResponse(json.dumps({'error': 'User has already downvoted this comment.'}), status=400)

    else:
        return HttpResponse(status=403)

@login_required
@no_professor_access
@csrf_protect
@api_view(['POST',])
def flag(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return HttpResponse(status=404)

    if review.flagged:
        return HttpResponse(status=403)

    form = FlagForm(request.POST)
    if form.is_valid():
        user = request.user
        review.flagged = True
        review.flagged_by = user
        review.flagged_count = F('flagged_count') + 1
        review.why_flag = form.cleaned_data['why_flag']
        review.save()

        review.send_flagged_email()

        serializer = CommentSerializer(review, context={'request': request})
        return Response(serializer.data)
    else:
        return HttpResponse(json.dumps({'errors': form.errors}), status=200)

def new_review_course_options(request):
    user_reviews = Review.objects.filter(user=request.user)
    user_prof_courses = [r.prof_course.pk for r in user_reviews]

    prof_courses = ProfCourse.objects.exclude(pk__in=user_prof_courses) \
        .values('prof__first', 'prof__last', 'course__title', 'course__code', 'id') \
        .order_by('course__code')

    options = [{'id': pc['id'],
                'text': pc['course__code'] + ': ' +
                        pc['course__title'] + ' with ' +
                        pc['prof__first'] + ' ' + pc['prof__last']} for pc in prof_courses]

    return HttpResponse(json.dumps(options), status=200)

# Helper methods to tokenize Professor, Course models
def get_course_tokens(course):
    """Return an array of single word tokens, given a course object."""
    tokens = []

    # Code
    code = course.code.split(' ')[0]
    tokens.append(code)

    # Department
    dept_name_array = course.dept.name.replace("of ", "").replace("and ", "").replace("& ", "").split(" ")
    tokens.extend(dept_name_array)

    # Title
    title_array = course.title.replace("to ", "").replace("of ", "").replace("in ", "").split(" ")
    tokens.extend(title_array)

    return tokens

def get_professor_tokens(professor):
    """Returns and array of single word tokens, given a professor object."""
    tokens = []

    # Name
    tokens.append(professor.first)
    tokens.append(professor.last)

    # Department
    dept_name_array = professor.dept.name.replace("of ", "").replace("and ", "").replace("& ", "").split(" ")
    tokens.extend(dept_name_array)

    # Email
    tokens.append(professor.email)

    return tokens
