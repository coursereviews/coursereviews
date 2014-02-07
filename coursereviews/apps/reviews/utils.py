from django.utils.dateformat import DateFormat
from reviews.models import Review

import datetime
import json

class Review_Aggregator:
    """Aggregate all the reviews for a professor 
       or course and prepare for d3.js charts."""
    def __init__(self, reviews):
        self.reviews = reviews

        # Initialize with keys that will be present regardless
        # of course or professor, avoids KeyErrors in the aggregators.
        # comments is an array of strings, date is a datetime.date
        # date is initialized as wayyyyy back (Unix Epoch)
        self.aggregate_values = {'comments': [], 'date': datetime.date(1970, 1, 1)}

    def aggregate(self):
        map(self.aggregate_review, self.reviews)

        # Format the date as "February 2, 2014"
        df = DateFormat(self.aggregate_values['date'])
        self.aggregate_values['date'] = df.format('F j, Y')

        return json.dumps(self.aggregate_values)

    def aggregate_review(self, review):

        # Don't serialize 'user_id' and 'id'
        review.pop('user_id', None)
        review.pop('id', None)

        # Iterate over fields
        for field in review:
            if field in ('components', 'value', 'why_take'):
                self.multi_choice_aggregator(review, field)
            elif field in ('again', 'another', 'grasp'):
                self.single_choice_aggregator(review, field)
            elif field is 'date':
                self.most_recent_date(review['date'])
            elif field is 'comment':
                self.comment_aggregator(review['comment'])
            else:
                self.integer_aggregator(review, field)

    def multi_choice_aggregator(self, review, field):
        """Aggregates the select multiple choice fields from each review."""

        components_choices = dict(Review.COMPONENTS_CHOICES)
        value_choices = dict(Review.VALUABLE_CHOICES)
        why_take_choices = dict(Review.WHY_TAKE_CHOICES)

        if field not in self.aggregate_values:
            self.aggregate_values[field] = {}

        # Assign choices based on field name
        if field is 'components':
            choices = components_choices
        elif field is 'value':
            choices = value_choices
        else:
            choices = why_take_choices

        # Select multiple fields are stored in the db
        # as comma delimited strings: 'A,B,C'.
        # Make a list of the values
        values = review[field].split(',')

        for value in values:
            full_value_name = choices[value]

            try:
                self.aggregate_values[field][full_value_name] += 1
            except KeyError:
                self.aggregate_values[field][full_value_name] = 1

    def single_choice_aggregator(self, review, field):
        """Aggregates the select single choice fields from each review."""

        again_choices = another_choices = dict(Review.YES_NO_CHOICES)
        grasp_choices = dict(Review.DESERVING_CHOICES)

        if field not in self.aggregate_values:
            self.aggregate_values[field] = {}

        # Assign choices based on field name
        if field in ('again', 'another'):
            choices = again_choices
        else:
            choices = grasp_choices

        full_value_name = choices[review[field]]

        try:
            self.aggregate_values[field][full_value_name] += 1
        except KeyError:
            self.aggregate_values[field][full_value_name] = 1

    def most_recent_date(self, date):
        """Updates `aggregate_values` with the date 
           of the most recent review."""

        if date > self.aggregate_values['date']:
            self.aggregate_values['date'] = date

    def comment_aggregator(self, comment):
        """Adds each comment to the `aggregate_values`."""

        self.aggregate_values['comments'].append(comment)

    def integer_aggregator(self, review, field):
        """Aggregates the integer fields from each review."""

        # Integer fields from Review model:
        # hours, prof_lecturing, prof_leading, prof_help, prof_feedback

        if field not in self.aggregate_values:
            self.aggregate_values[field] = {}

        try:
            self.aggregate_values[field][review[field]] += 1
        except KeyError:
            self.aggregate_values[field][review[field]] = 1
