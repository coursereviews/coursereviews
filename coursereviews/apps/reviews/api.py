from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import (Http404,
                         HttpResponse)

from reviews.models import (Review,
                            Professor,
                            Course)
from reviews.serializers import CommentSerializer

import json

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
