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
        # date is initialized as wayyyyy back
        self.aggregate_values = {'comments': [], 'date': datetime.date(1970, 1, 1)}

    def aggregate(self):
        map(self.aggregate_review, self.reviews)

        # Format the date as "February 2, 2014"
        df = DateFormat(self.aggregate_values['date'])
        self.aggregate_values['date'] = df.format('F j, Y')

        return json.dumps(self.aggregate_values)

    def aggregate_review(self, review):
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
        components_choices = dict(Review.COMPONENTS_CHOICES)
        value_choices = dict(Review.VALUABLE_CHOICES)
        why_take_choices = dict(Review.WHY_TAKE_CHOICES)

        print 'multi', field

    def single_choice_aggregator(self, review, field):
        again_choices = another_choices = dict(Review.YES_NO_CHOICES)
        grasp_choices = dict(Review.DESERVING_CHOICES)

        print 'single', field

    def most_recent_date(self, date):
        if date > self.aggregate_values['date']:
            self.aggregate_values['date'] = date

    def comment_aggregator(self, comment):
        self.aggregate_values['comments'].append(comment)

    def integer_aggregator(self, review, field):
        # hours, prof_lecturing, prof_leading, prof_help, prof_feedback

        print 'int', field

  