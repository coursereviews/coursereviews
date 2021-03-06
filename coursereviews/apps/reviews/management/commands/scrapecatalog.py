from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError
from django.utils.termcolors import colorize
from lxml import html
from lxml.cssselect import CSSSelector
from catalog.scraper import Scraper
from catalog.models import Term
import re
import requests
from reviews.models import Professor, Course, ProfCourse, Department

class Command(BaseCommand):
    help = 'Adds courses from the specified term to the database.'

    def __init__(self, *args, **kwargs):
        self.professors_added = 0
        self.courses_added = 0
        self.prof_courses_added = 0

        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('--term', help='Specify the term. Ex: 201590')
        parser.add_argument('--silent', action='store_true', help='Silence all output.')

    @staticmethod
    def validate_term(term):
        if not term:
            raise CommandError('No term given.')

        if len(term) != 6:
            raise CommandError('Term must be 6 digits. Ex: 201590.')

        try:
            int(term)
        except ValueError:
            raise CommandError('Term must contain only digits. Ex 201590.')

        term = Term(raw_id=term)
        if term.season == 'unknown':
            raise CommandError('Term contains invalid season.')

        return term

    @staticmethod
    def create_catalog(term):
        scraper = Scraper(term)
        scraper.xml_from_url()
        return scraper.create_catalog()

    @staticmethod
    def get_professor_by_id(id):
        """Get details about a Middlebury faculty member using their webid.

        Returns a dictionary of information about the professor if the request
        is successful, else returns an empty dictionary.
        """
        url = 'https://directory.middlebury.edu/GetRecord.aspx'
        res = requests.get(url, params={'webid': id})

        tree = html.fromstring(res.text)

        if not CSSSelector('tr')(tree)[0].text_content().strip():
            return None

        fields = []
        for tr in CSSSelector('tr')(tree):
            tds = tr.getchildren()
            fields.append((tds[0].text_content().strip(),
                           tds[1].text_content().strip()))

        return dict(fields)

    @staticmethod
    def course_is_skippable(course):
        """Check multiple conditions and return True if the course should not
        be added to MiddCourses.
        """

        conditions = (
            lambda: re.search('please register via', course.title, re.IGNORECASE),
            lambda: re.search('please register for', course.title, re.IGNORECASE),
            lambda: not any(course.instructors),
        )

        return any([condition() for condition in conditions])

    def get_or_create_professors(self, course):
        professors = []

        for instructor in course.instructors:
            # First try to get the Professor by midd_webid
            try:
                professor = Professor.objects.get(midd_webid=instructor.id)
                professors.append(professor)
                continue
            except Professor.DoesNotExist:
                pass

            # Then try to get the Professor by email and add its midd_webid
            professor_details = self.get_professor_by_id(instructor.id)
            if professor_details and 'E-mail' in professor_details:
                try:
                    professor = Professor.objects.get(email=professor_details['E-mail'])
                    professor.midd_webid = instructor.id
                    professor.save()
                    professors.append(professor)
                    continue
                except Professor.DoesNotExist:
                    pass

            # Unable to get a Professor by midd_webid or email.
            # Have to create a new Professor.
            if professor_details and 'E-mail' in professor_details:
                email = professor_details['E-mail']
            else:
                if not self.silent:
                    print(colorize('Unable to get email for Professor {}.'
                                   .format(instructor.name), fg='yellow'))
                email = None

            if professor_details and 'Department' in professor_details:
                department = professor_details['Department']
            else:
                department = course.department.text

            professor = Professor.objects.create(
                midd_webid=instructor.id,
                first=' '.join(instructor.name.split(' ')[:-1]),
                last=instructor.name.split(' ')[-1],
                email=email,
                dept=Department.objects.get_or_create(name=department)[0]
            )

            self.professors_added += 1

            if self.verbosity > 1:
                print('Added Professor {}.'.format(instructor.name))

            professors.append(professor)

        return professors

    def get_or_create_course(self, course):
        code_regex = re.compile(r'([A-Z]+[\d]+).*')
        code = code_regex.match(course.code).groups()[0]

        try:
            course = Course.objects.get(code=code)
        except Course.DoesNotExist:
            if course.description:
                description = html.fromstring(course.description).text_content()
            else:
                description = None

            course = Course.objects.create(
                code=code,
                title=course.title,
                description=description,
                dept=Department.objects.get_or_create(name=course.department.text)[0]
            )

            self.courses_added += 1

            if self.verbosity > 1:
                print('Added Course {}.'.format(code))
        return course

    def handle(self, *arguments, **options):
        self.verbosity = options['verbosity']
        self.silent = options['silent']

        term = self.validate_term(options['term'])
        catalog = self.create_catalog(term.id)

        for course in catalog:
            if self.course_is_skippable(course):
                continue

            professors = self.get_or_create_professors(course)
            course = self.get_or_create_course(course)

            for professor in professors:
                profcourse = ProfCourse.objects.get_or_create(
                    prof=professor,
                    course=course
                )

                if profcourse[1]:
                    self.prof_courses_added += 1

                    if self.verbosity > 1:
                        print('Added ProfCourse ({} {}, {}).'
                              .format(professor.first, professor.last, course.code))

        if not self.silent:
            print(colorize('Finished scraping term {}.'.format(options['term']), fg='green'))
            print(colorize('  Added {} Courses.'.format(self.courses_added), fg='blue'))
            print(colorize('  Added {} Professors.'.format(self.professors_added), fg='blue'))
            print(colorize('  Added {} ProfCourses'.format(self.prof_courses_added), fg='blue'))
