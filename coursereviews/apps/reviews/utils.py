from django.core import serializers
from reviews.models import Review

class Review_Aggregator:
    """Aggregate all the reviews for a professor 
        or course and prepare for d3.js charts."""
    def __init__(self, reviews):
        self.reviews = reviews
        print self.reviews

    def multi_choice_aggregator(self):
        components_choices = dict(Review.COMPONENTS_CHOICES)
        value_choices = dict(Review.VALUABLE_CHOICES)
        why_take_choices = dict(Review.WHY_TAKE_CHOICES)

    def single_choice_aggregator(self):
        again_choices = another_choices = dict(Review.YES_NO_CHOICES)
        grasp_choices = dict(Review.DESERVING_CHOICES)

    def integer_aggregator(self):
        # hours, prof_lecturing, prof_leading, prof_help, prof_feedback
        pass

  