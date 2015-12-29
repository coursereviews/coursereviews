from catalog.models import Course, Instructor
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from reviews.management.commands.scrapecatalog import Command as ScrapeCatalog

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
        course = Course()
        course.title = 'A valid title'
        course.instructors = [None]
        skippable = ScrapeCatalog.course_is_skippable(course)

        self.assertTrue(skippable)

    def test_course_is_skippable_please_register(self):
        course = Course()
        course.title = 'Please register via AMST0101'
        course.instructors = [Instructor()]
        self.assertTrue(ScrapeCatalog.course_is_skippable(course))

        course_strange_case = Course()
        course_strange_case.title = 'Please RegisteR via AMST0101'
        course_strange_case.instructors = [Instructor()]
        self.assertTrue(ScrapeCatalog.course_is_skippable(course_strange_case))

        course_for = Course()
        course_for.title = 'Please register for AMST0101'
        course_for.instructors = [Instructor()]
        self.assertTrue(ScrapeCatalog.course_is_skippable(course_for))

        course_for_strange_case = Course()
        course_for_strange_case.title = 'Please RegisteR for AMST0101'
        course_for_strange_case.instructors = [Instructor()]
        self.assertTrue(ScrapeCatalog.course_is_skippable(course_for_strange_case))

    def test_course_is_skippable_ok_course(self):
        course = Course()
        course.title = 'A valid title'
        course.instructors = [Instructor()]
        skippable = ScrapeCatalog.course_is_skippable(course)

        self.assertFalse(skippable)
