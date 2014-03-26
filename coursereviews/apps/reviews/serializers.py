from rest_framework import serializers
from reviews.models import Review

class CommentSerializer(serializers.ModelSerializer):
    vote_type = serializers.SerializerMethodField('user_vote_type')
    class Meta:
        model = Review
        exclude = (
            'prof_course', 'date', 'flagged_by',
            'flagged_count', 'components', 'again',
            'hours', 'another', 'grasp', 'prof_lecturing',
            'prof_leading', 'prof_feedback', 'prof_help',
            'value', 'why_take', 'user', 'up_votes', 'down_votes'
        )
    
    def user_vote_type(self, obj):
        """Returns `up` or `down` given a user and a review."""

        user = self.context['request'].user

        if user in obj.up_votes.all():
            return 'up'
        elif user in obj.down_votes.all():
            return 'down'
        else:
            return None