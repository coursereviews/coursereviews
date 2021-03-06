from datetime import date, timedelta
import json

from django.template.response import TemplateResponse
from django.db.models import Count
from django.contrib.auth.models import User
import pandas as pd

from reviews.models import Review, Course, Professor

def stats(request):
    start_date = date.today() - timedelta(days=29)

    reviews = Review.objects.filter(date__gte=start_date) \
        .values('date').annotate(count=Count('id')).order_by('date')

    context = {'start_date': start_date}

    s_reviews = pd.Series(
        map(lambda r: r['count'], reviews.values('count')),
        index=map(lambda r: r['date'], reviews.values('date'))) \
        .reindex(index=pd.date_range(start_date, periods=30), fill_value=0)

    context['review_stats'] = json.dumps(zip(
        s_reviews.index.map(lambda t: t.strftime('%Y-%m-%d')),
        s_reviews.tolist()))
    context['review_count'] = sum(s_reviews.tolist())

    users = User.objects.filter(date_joined__gte=start_date) \
        .extra({'date': 'date(date_joined)'}) \
        .values('date').annotate(count=Count('id'))

    sorted(users, key=lambda u: u['date'])

    s_users = pd.Series(
        map(lambda u: u['count'], users.values('date', 'count')),
        index=map(lambda u: u['date'], users.values('date', 'count'))) \
        .reindex(index=pd.date_range(start_date, periods=30), fill_value=0)

    context['user_stats'] = json.dumps(zip(
        s_users.index.map(lambda t: t.strftime('%Y-%m-%d')),
        s_users.tolist()))
    context['user_count'] = sum(s_users.tolist())

    context['launch_date'] = Review.objects.get(id=1).date
    context['total_reviews'] = Review.objects.all().count()
    context['total_users'] = User.objects.all().count()
    context['total_courses'] = Course.objects.all().count()
    context['total_professors'] = Professor.objects.all().count()

    context['top_courses'] = Course.objects \
        .annotate(reviews=Count('prof_courses__reviews')) \
        .order_by('-reviews')[:10]

    context['top_professors'] = Professor.objects \
        .annotate(reviews=Count('prof_courses__reviews')) \
        .order_by('-reviews')[:10]

    return TemplateResponse(request, 'stats/stats.html', context)
