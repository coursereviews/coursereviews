from django.utils.dateformat import DateFormat
from reviews.models import Review, ProfCourse

import datetime
import json

class Review_Aggregator:
    """Aggregate all the reviews for a professor
       or course and prepare for d3.js charts."""
    def __init__(self, reviews, attach_comment_slug=False):
        self.reviews = reviews
        self.count = len(reviews)

        # If True, attach the slug of the course related to the comment
        self.attach_comment_slug = attach_comment_slug

        # Initialize with keys that will be present regardless
        # of course or professor, avoids KeyErrors in the aggregators.
        # comments is an array of strings, date is a datetime.date
        # date is initialized as wayyyyy back (Unix Epoch)
        self.aggregate_values = {}

    def aggregate(self, as_dict=False):
        map(self.aggregate_review, self.reviews)

        # Format the date as "February 2, 2014"
        if 'date' in self.aggregate_values:
            df = DateFormat(self.aggregate_values['date'])
            self.aggregate_values['date'] = df.format('F j, Y')

        if 'prof_course' in self.aggregate_values:
            self.aggregate_values.pop('prof_course', None)

        self.aggregate_values['count'] = self.count

        if as_dict:
            return self.aggregate_values
        else:
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
            elif field == 'date':
                self.most_recent_date(review['date'])
            elif field == 'comment':
                self.comment_aggregator(review, field)
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
        if field == 'components':
            choices = components_choices
        elif field == 'value':
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

        if 'date' not in self.aggregate_values:
            self.aggregate_values['date'] = datetime.date(1970, 1, 1)

        if date > self.aggregate_values['date']:
            self.aggregate_values['date'] = date

    def comment_aggregator(self, review, field):
        """Adds each comment to the `aggregate_values`."""

        if review[field]:

            if 'comments' not in self.aggregate_values:
                self.aggregate_values['comments'] = []

            if self.attach_comment_slug:
                prof_course = ProfCourse.objects.select_related('course').get(id=review['prof_course'])
                course_code = prof_course.course.code
                course_url = prof_course.course.get_absolute_url()

                self.aggregate_values['comments'].append({'comment': review[field], 'course_code': course_code, 'course_url': course_url})

            else:
                self.aggregate_values['comments'].append(review[field])

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
