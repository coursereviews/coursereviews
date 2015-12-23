from django.core.management.base import NoArgsCommand
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.models import User

from reviews.models import Review
from reviews.utils import Review_Aggregator

from textblob import TextBlob
import json

class Command(NoArgsCommand):
    help = "Collect and write out analytics."

    def handle_noargs(self, **options):
        reviews_count = Review.objects.all().count()

        comments_count = Review.objects.exclude(comment='').count()

        comments_hours = map(lambda r: {'comment': r['comment'], 'hours': r['hours']},
                             Review.objects.exclude(comment='').values('comment', 'hours'))

        comment_blobs = map(lambda r: {'blob': TextBlob(r['comment']), 'hours': r['hours']},
                            comments_hours)

        avg_comment_length = sum(map(lambda r: len(r['comment']),
                                 comments_hours)) / float(comments_count)

        comment_sentiment_hours = map(lambda r: {'subjectivity': r['blob'].sentiment.subjectivity,
                                                 'polarity': r['blob'].sentiment.polarity,
                                                 'hours': r['hours']}, comment_blobs)

        reviews_by_day = Review.objects.extra({'date': 'date(date)'}) \
            .values('date').annotate(count=Count('id'))

        for r in reviews_by_day:
            r['date'] = str(r['date'])

        reviews_by_day_comments = Review.objects.exclude(comment='').extra({'date': 'date(date)'}) \
            .values('date').annotate(count=Count('id'))

        for r in reviews_by_day_comments:
            r['date'] = str(r['date'])

        users_by_day = User.objects.extra({'date': 'date(date_joined)'}) \
            .values('date').annotate(count=Count('id'))

        for u in users_by_day:
            u['date'] = str(u['date'])

        hours_another = Review.objects.all().values('hours', 'another').annotate(count=Count('id'))
        hours_again = Review.objects.all().values('hours', 'again').annotate(count=Count('id'))
        hours_grade = Review.objects.all().values('hours', 'grasp').annotate(count=Count('id'))
        another_lecturing = Review.objects.all() \
            .values('another', 'prof_lecturing').annotate(count=Count('id'))
        another_leading = Review.objects.all() \
            .values('another', 'prof_leading').annotate(count=Count('id'))
        another_help = Review.objects.all() \
            .values('another', 'prof_help').annotate(count=Count('id'))
        another_feedback = Review.objects.all() \
            .values('another', 'prof_feedback').annotate(count=Count('id'))

        reviews_values = Review.objects.all().values('components', 'again',
                                                     'hours', 'another', 'grasp',
                                                     'prof_lecturing', 'prof_leading',
                                                     'prof_help', 'prof_feedback',
                                                     'value', 'why_take')

        aggregator = Review_Aggregator(reviews_values)
        aggregated_stats = aggregator.aggregate()

        # Need to call list on some to convert from QuerySet
        output = {'reviews_count': reviews_count,
                  'comments_count': comments_count,
                  'avg_comment_length': avg_comment_length,
                  'comment_sentiment_hours': comment_sentiment_hours,
                  'reviews_by_day': list(reviews_by_day),
                  'reviews_by_day_comments': list(reviews_by_day_comments),
                  'users_by_day': list(users_by_day),
                  'hours_another': list(hours_another),
                  'hours_again': list(hours_again),
                  'hours_grade': list(hours_grade),
                  'another_lecturing': list(another_lecturing),
                  'another_leading': list(another_leading),
                  'another_help': list(another_help),
                  'another_feedback': list(another_feedback),
                  'aggregated_values': aggregated_stats}

        file_path = settings.DJANGO_ROOT + "/static/cr_admin/"
        writer = open(file_path + 'analytics.json', 'w')
        json.dump(output, writer)
        writer.close()
