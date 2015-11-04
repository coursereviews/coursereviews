from django.test import TestCase
from reviews.models import (Department,
                            Professor,
                            Course)

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
        self.assertEqual(film.get_absolute_url(), '/#departments/{0}/film-media-culture'.format(film.id))

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

class CourseTestCase(TestCase):
    def setUp(self):
        dept = Department.objects.create(name='Computer Science')
        Course.objects.create(
            code='CSCI0101',
            title='Introduction to Computer Science',
            description='CS Description',
            dept=dept
        )

    def test_code(self):
        course = Course.objects.get_by_natural_key('CSCI0101')
        self.assertEqual(course.code, 'CSCI0101')

    def test_title(self):
        course = Course.objects.get_by_natural_key('CSCI0101')
        self.assertEqual(course.title, 'Introduction to Computer Science')

    def test_description(self):
        course = Course.objects.get_by_natural_key('CSCI0101')
        self.assertEqual(course.description, 'CS Description')

    def test_department(self):
        course = Course.objects.get_by_natural_key('CSCI0101')
        dept = Department.objects.get(name='Computer Science')
        self.assertEqual(course.dept, dept)
        self.assertEqual(dept.courses.all()[0], course)

    def test_slug(self):
        course = Course.objects.get_by_natural_key('CSCI0101')
        self.assertEqual(course.slug, 'csci0101')

    def test_lookup(self):
        course = Course.objects.get_by_natural_key('CSCI0101')
        self.assertEqual(course.lookup, 'Introduction to Computer Science')

    def test_natural_key(self):
        course_by_natural_key = Course.objects.get_by_natural_key('CSCI0101')
        course_by_code = Course.objects.get(code='CSCI0101')
        self.assertEqual(course_by_natural_key, course_by_code)

    def test_absolute_url(self):
        course = Course.objects.get_by_natural_key('CSCI0101')
        self.assertEqual(course.get_absolute_url(),
            '/course/csci0101')

    def test_unicode(self):
        course = Course.objects.get_by_natural_key('CSCI0101')
        self.assertEqual(unicode(course),
            'CSCI0101 - Introduction to Computer Science')
