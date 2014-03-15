from rest_framework import serializers
from reviews.models import Review

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = (
            'prof_course', 'date', 'flagged_by',
            'flagged_count', 'components', 'again',
            'hours', 'another', 'grasp', 'prof_lecturing',
            'prof_leading', 'prof_feedback', 'prof_help',
            'value', 'why_take', 'user',
        )