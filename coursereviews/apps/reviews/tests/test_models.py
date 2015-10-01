from django.test import TestCase
from reviews.models import (Department,
                            Professor)

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

class ProfessorTestCase(TestCase):
    def setUp(self):
        dept = Department.objects.create(name='Computer Science')
        Professor.objects.create(
            first='FirstName',
            last='LastName',
            dept=dept,
            email='prof@middlebury.edu',
        )

    def test_first_name(self):
        prof = Professor.objects.get(last='LastName')
        self.assertEqual(prof.first, 'FirstName')

    def test_last_name(self):
        prof = Professor.objects.get(last='LastName')
        self.assertEqual(prof.last, 'LastName')

    def test_department(self):
        prof = Professor.objects.get(last='LastName')
        dept = Department.objects.get(name='Computer Science')
        self.assertEqual(prof.dept, dept)
        self.assertEqual(dept.professors.all()[0], prof)

    def test_email(self):
        prof = Professor.objects.get(last='LastName')
        self.assertEqual(prof.email, 'prof@middlebury.edu')

    def test_slug(self):
        prof = Professor.objects.get(last='LastName')
        self.assertEqual(prof.slug, 'firstname-lastname')

    def test_lookup(self):
        prof = Professor.objects.get(last='LastName')
        self.assertEqual(prof.lookup, 'FirstName LastName')

    def test_natural_key(self):
        prof = Professor.objects.get_by_natural_key('LastName')
        self.assertEqual(prof.first, 'FirstName')

    def test_absolute_url(self):
        prof = Professor.objects.get(last='LastName')
        self.assertEqual(prof.get_absolute_url(),
                         '/professor/firstname-lastname')

    def test_unicode(self):
        prof = Professor.objects.get(last='LastName')
        self.assertEqual(unicode(prof), 'FirstName LastName')
