from catalog.models import Course as CatalogCourse, Instructor
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from reviews.management.commands.scrapecatalog import Command as ScrapeCatalog
from reviews.models import Professor, Course, ProfCourse, Department

class ScrapecoursesTest(TestCase):
    def test_no_term(self):
        self.assertRaises(CommandError, lambda: call_command('scrapecatalog'))

    def test_term_wrong_length(self):
        self.assertRaises(CommandError,
                          lambda: call_command('scrapecatalog', term='2015'))
        self.assertRaises(CommandError,
                          lambda: call_command('scrapecatalog', term='2015901'))

    def test_term_no_digits(self):
        self.assertRaises(CommandError,
                          lambda: call_command('scrapecatalog', term='2015ab'))

    def test_term_bad_season(self):
        self.assertRaises(CommandError,
                          lambda: call_command('scrapecatalog', term='201501'))

    def test_create_catalog(self):
        catalog = ScrapeCatalog.create_catalog('201590')
        self.assertEqual(len(catalog.courses), 894)

    def test_get_professor_by_id(self):
        test_id = '1324ccafb6640fbdabc0c1f337a537d1'
        fields = ScrapeCatalog.get_professor_by_id(test_id)

        self.assertEqual(fields['Department'], 'Chemistry and Biochemistry')
        self.assertEqual(fields['E-mail'], 'kjewett@middlebury.edu')

    def test_get_professor_by_id_wrong_id(self):
        test_id = '1'
        fields = ScrapeCatalog.get_professor_by_id(test_id)

        self.assertEqual(fields, None)

    def test_course_is_skippable_no_professors(self):
        course = CatalogCourse()
        course.title = 'A valid title'
        course.instructors = [None]
        skippable = ScrapeCatalog.course_is_skippable(course)

        self.assertTrue(skippable)

    def test_course_is_skippable_please_register(self):
        course = CatalogCourse()
        course.title = 'Please register via AMST0101'
        course.instructors = [Instructor()]
        self.assertTrue(ScrapeCatalog.course_is_skippable(course))

        course_strange_case = CatalogCourse()
        course_strange_case.title = 'Please RegisteR via AMST0101'
        course_strange_case.instructors = [Instructor()]
        self.assertTrue(ScrapeCatalog.course_is_skippable(course_strange_case))

        course_for = CatalogCourse()
        course_for.title = 'Please register for AMST0101'
        course_for.instructors = [Instructor()]
        self.assertTrue(ScrapeCatalog.course_is_skippable(course_for))

        course_for_strange_case = CatalogCourse()
        course_for_strange_case.title = 'Please RegisteR for AMST0101'
        course_for_strange_case.instructors = [Instructor()]
        self.assertTrue(ScrapeCatalog.course_is_skippable(course_for_strange_case))

    def test_course_is_skippable_ok_course(self):
        course = CatalogCourse()
        course.title = 'A valid title'
        course.instructors = [Instructor()]
        skippable = ScrapeCatalog.course_is_skippable(course)

        self.assertFalse(skippable)

class ScrapecoursesIntegrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        dept = Department.objects.create(
            name='Program in American Studies'
        )

        course = Course.objects.create(
            code='AMST0102',
            title='Politics, Media, Popular Culture',
            dept=dept
        )

        professor = Professor.objects.create(
            midd_webid='eb22314a852970f29d9c828dec3265d2',
            email='hallen@middlebury.edu',
            first='Holly',
            last='Allen',
            dept=dept
        )

        Professor.objects.create(
            email='jfinley@middlebury.edu',
            first='J',
            last='Finley',
            dept=dept
        )

        ProfCourse.objects.create(
            course=course,
            prof=professor
        )

        call_command('scrapecatalog', term='201590', silent=True)

        super(ScrapecoursesIntegrationTest, cls).setUpClass()

    def test_all_profcourses_added(self):
        profcourses = ProfCourse.objects.all()

        self.assertEqual(len(profcourses), 544)

    def test_prof_with_existing_webid_not_created(self):
        profs = Professor.objects.filter(midd_webid='eb22314a852970f29d9c828dec3265d2')

        self.assertEqual(len(profs), 1)

    def test_prof_with_existing_email_not_created(self):
        profs = Professor.objects.filter(email='jfinley@middlebury.edu')

        self.assertEqual(len(profs), 1)

    def test_prof_with_existing_email_not_updated_with_webid(self):
        prof = Professor.objects.get(email='jfinley@middlebury.edu')

        self.assertEqual(prof.midd_webid, 'dea11cc8d58c932c8822532eb1b1d95e')

    def test_existing_course_not_created(self):
        courses = Course.objects.filter(code='AMST0102')

        self.assertEqual(len(courses), 1)

    def test_existing_department_not_created(self):
        depts = Department.objects.filter(name='Program in American Studies')

        self.assertEqual(len(depts), 1)

    def test_existing_profcourse_not_created(self):
        course = Course.objects.get(code='AMST0102')
        prof = Professor.objects.get(midd_webid='eb22314a852970f29d9c828dec3265d2')
        profcourses = ProfCourse.objects.filter(course=course, prof=prof)

        self.assertEqual(len(profcourses), 1)

    def test_department_created(self):
        depts = Department.objects.filter(name='Computer Science')

        self.assertEqual(len(depts), 1)

    def test_course_created(self):
        courses = Course.objects.filter(code='AMST0204')

        self.assertEqual(len(courses), 1)

    def test_prof_created(self):
        profs = Professor.objects.filter(midd_webid='e1aa26eece8d090367ff654d1f517c7a')

        self.assertEqual(len(profs), 1)
        self.assertEqual(profs[0].email, 'efoutch@middlebury.edu')
        self.assertEqual(profs[0].first, 'Ellery')
        self.assertEqual(profs[0].last, 'Foutch')
        self.assertEqual(profs[0].dept.name, 'American Studies')
