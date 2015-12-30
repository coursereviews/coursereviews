"""Pad existing codes on Courses with zeros between department and course codes.

This is a one off script written for the transition from the scrapecourses
command to the Middlebury catalog module.

See https://github.com/coursereviews/coursereviews/issues/92
"""

from __future__ import print_function

from django.core.management.base import BaseCommand
import re
from reviews.models import Course

class Command(BaseCommand):
    help = 'Pad existing codes with zeros between department and course codes.'

    @staticmethod
    def needs_padding(code):
        """Check if a course code needs padding at the front of the course number.

        >>> needs_padding('AMST101')
        True

        >>> needs_padding('AMST0101')
        False
        """

        regex = re.compile(r'[A-Z]+(\d+)')
        digits = regex.match(code).groups()[0]

        return len(digits) < 4

    @staticmethod
    def pad_code(code):
        """Pad code with zeros between department and course codes.

        >>> pad_code('AMST101')
        AMST101

        >>> pad_code('ART101')
        ART0101
        """

        regex = re.compile(r'([A-Z]+)(\d+)')
        department, course = regex.match(code).groups()

        zeros_needed = 4 - len(course)
        course = '0' * zeros_needed + course

        return ''.join((department, course))

    def handle(self, *arguments, **options):
        self.verbosity = options.get('verbosity')

        courses = Course.objects.all()

        for course in courses:
            if self.needs_padding(course.code):
                padded = self.pad_code(course.code)

                if self.verbosity > 1:
                    print('{:>8} --> {}'.format(course.code, padded))

                course.code = padded
                course.save()
