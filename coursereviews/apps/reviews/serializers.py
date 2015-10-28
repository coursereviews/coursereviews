from rest_framework import serializers
from reviews.models import (Review,
                            Department,
                            Course,
                            Professor)

class CommentSerializer(serializers.ModelSerializer):
    vote_type = serializers.SerializerMethodField('user_vote_type')
    class Meta:
        model = Review
        exclude = (
            'prof_course', 'date', 'flagged_by',
            'flagged_count', 'flagged_mod', 'why_flag',
            'components', 'again', 'hours', 'another',
            'grasp', 'prof_lecturing', 'prof_leading',
            'prof_feedback', 'prof_help', 'value', 'why_take',
            'user', 'up_votes', 'down_votes',
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

class DepartmentSerializer(serializers.ModelSerializer):
    has_professors = serializers.SerializerMethodField()
    has_courses = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        exclude = ('description',)

    def get_has_professors(self, obj):
        return len(obj.professors.all()) > 0

    def get_has_courses(self, obj):
        return len(obj.courses.all()) > 0

    def get_reviews_count(self, obj):
        return Review.objects.filter(prof_course__course__dept=obj).count()

class CourseSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('code', 'dept', 'id', 'reviews_count', 'slug', 'title')

    def get_reviews_count(self, obj):
        return Review.objects.filter(prof_course__course__id=obj.id).count()

class ProfessorSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Professor
        fields = ('slug', 'id', 'name', 'reviews_count', 'dept')

    def get_name(self, obj):
        return unicode(obj)

    def get_reviews_count(self, obj):
        return Review.objects.filter(prof_course__prof__id=obj.id).count()
