from datetime import date, timedelta
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from reviews.models import Department, Review, Professor, Course, ProfCourse

def get_department():
    return Department.objects.get_or_create(
        name='Computer Science'
    )[0]

def get_professor():
    return Professor.objects.get_or_create(
        first='CS',
        last='Professor',
        dept=get_department()
    )[0]

def get_course():
    return Course.objects.get_or_create(
        code='CSCI101',
        title='Intro to Computer Science',
        dept=get_department()
    )[0]

def get_prof_course():
    return ProfCourse.objects.get_or_create(
        course=get_course(),
        prof=get_professor()
    )[0]

class StatsViewTests(TestCase):
    def setUp(self):
        User.objects.create(username='test', password='test')
        self.client.login(username='test', password='test')

        user = User.objects.get(username='test')
        Review.objects.create(
            user=user,
            prof_course=get_prof_course(),
            components='A,B',
            again='Y',
            hours=5,
            another='Y',
            grasp='A',
            prof_lecturing='5',
            prof_leading='5',
            prof_help='4',
            prof_feedback='4',
            value='P,W',
            why_take='A,I'
        )

    def test_stats_view(self):
        response = self.client.get(reverse('stats.stats'))
        today = date.today().strftime('%m/%d/%Y')
        last_month = (date.today() - timedelta(days=29)).strftime('%m/%d/%Y')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Totals since {0}'.format(today))
        self.assertContains(response, 'Last 30 days starting {0}'.format(last_month))
        self.assertContains(response, 'CS Professor'),
        self.assertContains(response, 'CSCI101 - Intro to Computer Science')
