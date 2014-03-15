from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import Http404

from reviews.models import Review
from reviews.serializers import CommentSerializer

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
