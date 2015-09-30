from django.test import TestCase
from reviews.models import Department

class DepartmentTestCase(TestCase):
    def setUp(self):
        Department.objects.create(name='Film & Media Culture',
                                  display_name='Film and Media Culture')
        Department.objects.create(name='Computer Science')

    def test_unicode(self):
        film = Department.objects.get(name='Film & Media Culture')
        cs = Department.objects.get(name='Computer Science')

        # Object with a different display_name
        self.assertEqual(unicode(film), 'Film and Media Culture')

        # Object with no display_name
        self.assertEqual(unicode(cs), 'Computer Science')

    def test_slugify(self):
        film = Department.objects.get(name='Film & Media Culture')
        self.assertEqual(film.slug, 'film-media-culture')

    def test_absolute_url(self):
        film = Department.objects.get(name='Film & Media Culture')
        self.assertEqual(film.get_absolute_url(), '/#film-media-culture')