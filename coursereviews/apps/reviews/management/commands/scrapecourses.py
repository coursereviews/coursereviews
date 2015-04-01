from django.core.management.base import BaseCommand, CommandError

from reviews.models import (Professor,
                            Course,
                            ProfCourse,
                            Department)

import requests
from bs4 import BeautifulSoup

import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Command(BaseCommand):
    args = '<term>'
    help = """Scrapes all courses and professors from middlebury.edu.

Requires the term as the first and only argument.  Get the
course by visiting the appropriate Middlebury course catalog
page and getting the value of the url parameter 'p_term'."""

    def __init__(self, *args, **kwargs):
        self.term = ''

        # Need prof_dept and course_dept variables for the dept from the try/except
        # in the professor and course scrapers so we can save it for the professor/course
        self.prof_dept = Department()
        self.course_dept = Department()

        self.course = Course()
        self.professor = Professor()

        self.description = ''

        self.instructor_first = ''
        self.instructor_last = ''

        # We make a few attempts to clean up and unify the database
        # Don't add any high level research/thesis courses,
        # discussion sections, labs, drills, or cross references
        self.bad_course_names = ('Advanced Studies',
                                 'Advanced Study',
                                 'Adv Individual Study',
                                 'Independent',
                                 'Ind.',
                                 'Indep.',
                                 'Indep Project',
                                 'Thesis',
                                 'Research',
                                 'Resrch',
                                 'Senior',
                                 'Sr Essay',
                                 'Sr. Thesis',
                                 'Honors',
                                 'Special Project',
                                 'Advanced Study',
                                 'Please register via',
                                 'Discussion',
                                 'Drill')

        # Aliases for inconsistent department names
        self.aliases = {
                        'Center Comparative Study of Race & Ethnicity': 'Center Comparative Study of Race and Ethnicity',
                        "Chemistry and Biochemistry/Dean of Faculty's Office": 'Chemistry and Biochemistry',
                        'Computer Science/Commons Office - Cook': 'Computer Science',
                        'Molecular Biology  & Biochem': 'Chemistry and Biochemistry',
                        'Molecular Biology & Biochem': 'Chemistry and Biochemistry',
                        'Classics/Commons Office - Ross': 'Classics',
                        'Economics/Creativity & Innovation': 'Economics',
                        'Education Studies/Commons Office - Wonnacott': 'Education Studies',
                        'English & American Literatures': 'English and American Literatures',
                        'Environmental Affairs': 'Environmental Studies',
                        'Environmental Studies/Biology': 'Environmental Studies',
                        'Environmental Studies/History': 'Environmental Studies',
                        'Film & Media Culture': 'Film and Media Culture',
                        'Gender, Sexuality & Feminist Studies': 'Gender, Sexuality, and Feminist Studies',
                        'Gender Sexuality &Fem. Studies': 'Gender, Sexuality, and Feminist Studies',
                        'Gender Sexuality &Fem.; Studies': 'Gender, Sexuality, and Feminist Studies',
                        'Geography/Commons Office - Atwater': 'Geography',
                        'German/Commons Office - Brainerd': 'German',
                        'Hebrew (Modern)': 'Hebrew',
                        'Hebrew (Classical)': 'Hebrew',
                        'History of Art & Architecture': 'History of Art and Architecture',
                        'History of Art & Architecture/Arts Center': 'History of Art and Architecture',
                        'Dean of Students/History of Art & Architecture': 'History of Art and Architecture',
                        'International & Global Studies': 'International and Global Studies',
                        'International Studies': 'International and Global Studies',
                        'Italian/Commons Office - Cook': 'Italian',
                        'Italian/Commons Office - Brainerd': 'Italian',
                        'Italian/Italian School': 'Italian',
                        'Japanese Studies': 'Japenese',
                        'Planning and Assessment/Psychology': 'Psychology',
                        'Religion/Classics': 'Religion',
                        'Religion/Commons Office - Ross': 'Religion',
                        "Women's & Gender Studies": "Women's and Gender Studies",
                        u'\xa0': ' '
                        }

        self.bad_departments = ('Chinese School',
                                'German School',
                                'Russian School',
                                'Spanish School',
                                'Portuguese School',
                                'Italian School',
                                'Language Schools at Mills',
                                'Internship',
                                'Winter Term')

        self.prof_count = 0
        self.dept_count = 0
        self.course_count = 0
        self.prof_course_count = 0

        super(Command, self).__init__()

    def handle(self, *args, **options):
        if len(args) == 1:
            self.term = args[0]
        else:
            raise CommandError('scrapeprofs requires exactly one argument, got %s.' % len(args))

        # Scrape the professors
        self.stdout.write(bcolors.HEADER + 'Scraping professors . . .' + bcolors.ENDC)

        # Make an extensive post request for the professors
        profs_payload = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUJMzg4Nzc1MDE5D2QWAmYPZBYCZg9kFggCBw9kFgJmDxYCHgRUZXh0BYQGICAgIDxoZWFkZXIgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgIAogICAgICA8Zm9ybSBjbGFzcz0ic2VhcmNoIiBhY3Rpb249Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvc2VhcmNoIiBtZXRob2Q9ImdldCIgdGFyZ2V0PSJfdG9wIj4KICAgICAgICA8bGFiZWwgZm9yPSJtaWRkX3NlYXJjaF9xdWVyeSI+U2VhcmNoIE1pZGQ8L2xhYmVsPgogICAgICAgIDxpbnB1dCB0eXBlPSJzZWFyY2giIGlkPSJtaWRkX3NlYXJjaF9xdWVyeSIgY2xhc3M9InNlYXJjaF9xdWVyeSB4LXdlYmtpdC1zcGVlY2giIG5hbWU9InEyIiBwbGFjZWhvbGRlcj0iU2VhcmNoIE1pZGQiIHgtd2Via2l0LXNwZWVjaCByZXF1aXJlZD4KICAgICAgICA8aW5wdXQgdHlwZT0ic3VibWl0IiBpZD0ibWlkZF9zZWFyY2hfc3VibWl0IiBjbGFzcz0ic2VhcmNoX3N1Ym1pdCIgdmFsdWU9IkdvIj4KICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBpZD0ibWlkZF9hamF4X3NlYXJjaF91cmwiIHZhbHVlPSJodHRwOi8vd3d3Lm1pZGRsZWJ1cnkuZWR1L2dvL3NlYXJjaCI+CiAgICAgIDwvZm9ybT4KICAgICAgPGgxIGlkPSJtaWRkX3dvcmRtYXJrIiBjbGFzcz0id29yZG1hcmsiPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUiPjxpbWcgc3JjPSIvL2Nkbi5taWRkbGVidXJ5LmVkdS9taWRkbGVidXJ5LmVkdS8yMDEwL2ltYWdlcy9sb2dvLnBuZz8yMDE1LTAxLTA3IiB3aWR0aD0iMzgwIiBoZWlnaHQ9IjExMCIgYWx0PSJNaWRkbGVidXJ5Ij48L2E+PC9oMT4KICAgIDwvaGVhZGVyPmQCCQ9kFgJmDxYCHwAF2wwgICAgPG5hdiBpZD0ibWlkZF9uYXZpZ2F0aW9uIiBjbGFzcz0ibmF2aWdhdGlvbiBjb250YWluZXIiPgogICAgICA8dWw+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfYWRtaXNzaW9ucyB0b3AiPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvYWRtaXNzaW9ucyI+QWRtaXNzaW9uczxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICA8bGkgY2xhc3M9Im5hdl9hY2FkZW1pY3MgdG9wIj48YSBocmVmPSJodHRwOi8vd3d3Lm1pZGRsZWJ1cnkuZWR1L2FjYWRlbWljcyI+QWNhZGVtaWNzPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2X3N0dWRlbnRsaWZlIHRvcCI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9zdHVkZW50bGlmZSI+U3R1ZGVudCBMaWZlPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2X2F0aGxldGljcyB0b3AiPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvYXRobGV0aWNzIj5BdGhsZXRpY3M8c3Bhbj48L3NwYW4+PC9hPjwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfYXJ0cyB0b3AiPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvYXJ0cyI+QXJ0czxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICA8bGkgY2xhc3M9Im5hdl9pbnRlcm5hdGlvbmFsIHRvcCI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9pbnRlcm5hdGlvbmFsIj5NaWRkbGVidXJ5IEludGVybmF0aW9uYWw8c3Bhbj48L3NwYW4+PC9hPjwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfbWlkZGxhYiB0b3AiPjxhIGhyZWY9Imh0dHA6Ly9taWRkbGFiLm1pZGRsZWJ1cnkuZWR1LyI+TWlkZExhYjxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICA8bGkgY2xhc3M9Im5hdl9hYm91dCBib3R0b20iPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvYWJvdXQiPkFib3V0PHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2X3N1c3RhaW5hYmlsaXR5IGJvdHRvbSI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9zdXN0YWluYWJpbGl0eSI+U3VzdGFpbmFiaWxpdHk8c3Bhbj48L3NwYW4+PC9hPjwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfZ2l2aW5nIGJvdHRvbSI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9naXZpbmciPkdpdmluZzxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICA8bGkgY2xhc3M9Im5hdl9uZXdzIGJvdHRvbSI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9uZXdzcm9vbSI+TmV3cyBSb29tPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2X2V2ZW50cyBib3R0b20iPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvZXZlbnRzIj5DYWxlbmRhciBvZiBFdmVudHM8c3Bhbj48L3NwYW4+PC9hPjwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfb2ZmaWNlcyBib3R0b20iPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvb2ZmaWNlcyI+T2ZmaWNlICZhbXA7IFNlcnZpY2VzPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICA8L3VsPgogICAgPC9uYXY+ZAILD2QWAgIBD2QWAgIDD2QWAmYPZBYGAgEPZBYCAhsPEGQPFndmAgECAgIDAgQCBQIGAgcCCAIJAgoCCwIMAg0CDgIPAhACEQISAhMCFAIVAhYCFwIYAhkCGgIbAhwCHQIeAh8CIAIhAiICIwIkAiUCJgInAigCKQIqAisCLAItAi4CLwIwAjECMgIzAjQCNQI2AjcCOAI5AjoCOwI8Aj0CPgI/AkACQQJCAkMCRAJFAkYCRwJIAkkCSgJLAkwCTQJOAk8CUAJRAlICUwJUAlUCVgJXAlgCWQJaAlsCXAJdAl4CXwJgAmECYgJjAmQCZQJmAmcCaAJpAmoCawJsAm0CbgJvAnACcQJyAnMCdAJ1AnYWdxAFDkFueSBEZXBhcnRtZW50ZWcQBRBBY2FkZW1pYyBBZmZhaXJzBRBBY2FkZW1pYyBBZmZhaXJzZxAFCkFkbWlzc2lvbnMFCkFkbWlzc2lvbnNnEAUQQW1lcmljYW4gU3R1ZGllcwUQQW1lcmljYW4gU3R1ZGllc2cQBQZBcmFiaWMFBkFyYWJpY2cQBQtBcnRzIENlbnRlcgULQXJ0cyBDZW50ZXJnEAUcQXNzaXN0YW50IFRyZWFzdXJlcidzIE9mZmljZQUcQXNzaXN0YW50IFRyZWFzdXJlcidzIE9mZmljZWcQBQlBdGhsZXRpY3MFCUF0aGxldGljc2cQBSZBdGhsZXRpY3MvQ29tbXVuaWNhdGlvbnMgYW5kIE1hcmtldGluZwUmQXRobGV0aWNzL0NvbW11bmljYXRpb25zIGFuZCBNYXJrZXRpbmdnEAUHQmlvbG9neQUHQmlvbG9neWcQBRxCcmVhZCBMb2FmIFNjaG9vbCBvZiBFbmdsaXNoBRxCcmVhZCBMb2FmIFNjaG9vbCBvZiBFbmdsaXNoZxAFHkJyZWFkIExvYWYgV3JpdGVycycgQ29uZmVyZW5jZQUeQnJlYWQgTG9hZiBXcml0ZXJzJyBDb25mZXJlbmNlZxAFDUJ1ZGdldCBPZmZpY2UFDUJ1ZGdldCBPZmZpY2VnEAUPQnVzaW5lc3MgT2ZmaWNlBQ9CdXNpbmVzcyBPZmZpY2VnEAUiQ2VudGVyIGZvciBDYXJlZXJzIGFuZCBJbnRlcm5zaGlwcwUiQ2VudGVyIGZvciBDYXJlZXJzIGFuZCBJbnRlcm5zaGlwc2cQBSVDZW50ZXIgZm9yIENvdW5zZWxpbmcvSHVtYW4gUmVsYXRpb25zBSVDZW50ZXIgZm9yIENvdW5zZWxpbmcvSHVtYW4gUmVsYXRpb25zZxAFJUNlbnRlciBmb3IgVGVhY2hpbmcvTGVhcm5pbmcvUmVzZWFyY2gFJUNlbnRlciBmb3IgVGVhY2hpbmcvTGVhcm5pbmcvUmVzZWFyY2hnEAURQ2hhcGxhaW4ncyBPZmZpY2UFEUNoYXBsYWluJ3MgT2ZmaWNlZxAFGkNoZW1pc3RyeSBhbmQgQmlvY2hlbWlzdHJ5BRpDaGVtaXN0cnkgYW5kIEJpb2NoZW1pc3RyeWcQBQdDaGluZXNlBQdDaGluZXNlZxAFDkNoaW5lc2UgU2Nob29sBQ5DaGluZXNlIFNjaG9vbGcQBQhDbGFzc2ljcwUIQ2xhc3NpY3NnEAUNQ29sbGVnZSBTdG9yZQUNQ29sbGVnZSBTdG9yZWcQBRhDb21tb25zIE9mZmljZSAtIEF0d2F0ZXIFGENvbW1vbnMgT2ZmaWNlIC0gQXR3YXRlcmcQBRlDb21tb25zIE9mZmljZSAtIEJyYWluZXJkBRlDb21tb25zIE9mZmljZSAtIEJyYWluZXJkZxAFFUNvbW1vbnMgT2ZmaWNlIC0gQ29vawUVQ29tbW9ucyBPZmZpY2UgLSBDb29rZxAFFUNvbW1vbnMgT2ZmaWNlIC0gUm9zcwUVQ29tbW9ucyBPZmZpY2UgLSBSb3NzZxAFGkNvbW1vbnMgT2ZmaWNlIC0gV29ubmFjb3R0BRpDb21tb25zIE9mZmljZSAtIFdvbm5hY290dGcQBRxDb21tdW5pY2F0aW9ucyBhbmQgTWFya2V0aW5nBRxDb21tdW5pY2F0aW9ucyBhbmQgTWFya2V0aW5nZxAFFENvbW11bml0eSBFbmdhZ2VtZW50BRRDb21tdW5pdHkgRW5nYWdlbWVudGcQBRBDb21wdXRlciBTY2llbmNlBRBDb21wdXRlciBTY2llbmNlZxAFJkNvbXB1dGVyIFNjaWVuY2UvQ29tbW9ucyBPZmZpY2UgLSBDb29rBSZDb21wdXRlciBTY2llbmNlL0NvbW1vbnMgT2ZmaWNlIC0gQ29va2cQBRNDb250cm9sbGVyJ3MgT2ZmaWNlBRNDb250cm9sbGVyJ3MgT2ZmaWNlZxAFF0NyZWF0aXZpdHkgJiBJbm5vdmF0aW9uBRdDcmVhdGl2aXR5ICYgSW5ub3ZhdGlvbmcQBS1DdHIgZm9yIENhbXB1cyBBY3Rpdml0aWVzICYgTGVhZGVyc2hpcCAoQ0NBTCkFLUN0ciBmb3IgQ2FtcHVzIEFjdGl2aXRpZXMgJiBMZWFkZXJzaGlwIChDQ0FMKWcQBQVEYW5jZQUFRGFuY2VnEAUrRGF2aXMgVW5pdGVkIFdvcmxkIENvbGxlZ2UgU2Nob2xhcnMgUHJvZ3JhbQUrRGF2aXMgVW5pdGVkIFdvcmxkIENvbGxlZ2UgU2Nob2xhcnMgUHJvZ3JhbWcQBRBEZWFuIG9mIFN0dWRlbnRzBRBEZWFuIG9mIFN0dWRlbnRzZxAFE0RlYW4gb2YgdGhlIENvbGxlZ2UFE0RlYW4gb2YgdGhlIENvbGxlZ2VnEAUPRGluaW5nIFNlcnZpY2VzBQ9EaW5pbmcgU2VydmljZXNnEAUJRWNvbm9taWNzBQlFY29ub21pY3NnEAUlRWNvbm9taWNzL0N0ciBTb2NpYWwgRW50cmVwcmVuZXVyc2hpcAUlRWNvbm9taWNzL0N0ciBTb2NpYWwgRW50cmVwcmVuZXVyc2hpcGcQBRJFY29ub21pY3MvTWlkZENPUkUFEkVjb25vbWljcy9NaWRkQ09SRWcQBRFFZHVjYXRpb24gU3R1ZGllcwURRWR1Y2F0aW9uIFN0dWRpZXNnEAUuRUlBOiBDYXJlZXJzLCBGZWxsb3dzaGlwcyBhbmQgQ2l2aWMgRW5nYWdlbWVudAUuRUlBOiBDYXJlZXJzLCBGZWxsb3dzaGlwcyBhbmQgQ2l2aWMgRW5nYWdlbWVudGcQBR5FbmdsaXNoICYgQW1lcmljYW4gTGl0ZXJhdHVyZXMFHkVuZ2xpc2ggJiBBbWVyaWNhbiBMaXRlcmF0dXJlc2cQBRVFbnZpcm9ubWVudGFsIEFmZmFpcnMFFUVudmlyb25tZW50YWwgQWZmYWlyc2cQBRVFbnZpcm9ubWVudGFsIFN0dWRpZXMFFUVudmlyb25tZW50YWwgU3R1ZGllc2cQBRFFdmVudHMgTWFuYWdlbWVudAURRXZlbnRzIE1hbmFnZW1lbnRnEAUTRmFjaWxpdGllcyBTZXJ2aWNlcwUTRmFjaWxpdGllcyBTZXJ2aWNlc2cQBSBGYWNpbGl0aWVzIFNlcnZpY2VzIC0gQnJlYWQgTG9hZgUgRmFjaWxpdGllcyBTZXJ2aWNlcyAtIEJyZWFkIExvYWZnEAUyRmFjaWxpdGllcyBTZXJ2aWNlcy9GYWNpbGl0aWVzIFNlcnZpY2VzLUJyZWFkIExvYWYFMkZhY2lsaXRpZXMgU2VydmljZXMvRmFjaWxpdGllcyBTZXJ2aWNlcy1CcmVhZCBMb2FmZxAFFkZpbG0gYW5kIE1lZGlhIEN1bHR1cmUFFkZpbG0gYW5kIE1lZGlhIEN1bHR1cmVnEAUGRnJlbmNoBQZGcmVuY2hnEAUNRnJlbmNoIFNjaG9vbAUNRnJlbmNoIFNjaG9vbGcQBSRHZW5kZXIsIFNleHVhbGl0eSAmIEZlbWluaXN0IFN0dWRpZXMFJEdlbmRlciwgU2V4dWFsaXR5ICYgRmVtaW5pc3QgU3R1ZGllc2cQBQlHZW9ncmFwaHkFCUdlb2dyYXBoeWcQBQdHZW9sb2d5BQdHZW9sb2d5ZxAFBkdlcm1hbgUGR2VybWFuZxAFC0dvbGYgQ291cnNlBQtHb2xmIENvdXJzZWcQBRtHcmFudHMgJiBTcG9uc29yZWQgUHJvZ3JhbXMFG0dyYW50cyAmIFNwb25zb3JlZCBQcm9ncmFtc2cQBQdIaXN0b3J5BQdIaXN0b3J5ZxAFHUhpc3Rvcnkgb2YgQXJ0ICYgQXJjaGl0ZWN0dXJlBR1IaXN0b3J5IG9mIEFydCAmIEFyY2hpdGVjdHVyZWcQBQ9IdW1hbiBSZXNvdXJjZXMFD0h1bWFuIFJlc291cmNlc2cQBQpIdW1hbml0aWVzBQpIdW1hbml0aWVzZxAFH0luZm9ybWF0aW9uIFRlY2hub2xvZ3kgU2VydmljZXMFH0luZm9ybWF0aW9uIFRlY2hub2xvZ3kgU2VydmljZXNnEAUnSW5zdGl0dXRlIGZvciB0aGUgQWR2YW5jZW1lbnQgb2YgSGVicmV3BSdJbnN0aXR1dGUgZm9yIHRoZSBBZHZhbmNlbWVudCBvZiBIZWJyZXdnEAUeSW50ZXJuYXRpb25hbCAmIEdsb2JhbCBTdHVkaWVzBR5JbnRlcm5hdGlvbmFsICYgR2xvYmFsIFN0dWRpZXNnEAUpSW50ZXJuYXRpb25hbCBQcm9ncmFtcyAmIE9mZi1DYW1wdXMgU3R1ZHkFKUludGVybmF0aW9uYWwgUHJvZ3JhbXMgJiBPZmYtQ2FtcHVzIFN0dWR5ZxAFKEludGVybmF0aW9uYWwgU3R1ZGVudCAmIFNjaG9sYXIgU2VydmljZXMFKEludGVybmF0aW9uYWwgU3R1ZGVudCAmIFNjaG9sYXIgU2VydmljZXNnEAUHSXRhbGlhbgUHSXRhbGlhbmcQBSFJdGFsaWFuL0NvbW1vbnMgT2ZmaWNlIC0gQnJhaW5lcmQFIUl0YWxpYW4vQ29tbW9ucyBPZmZpY2UgLSBCcmFpbmVyZGcQBQ9KYXBhbmVzZSBTY2hvb2wFD0phcGFuZXNlIFNjaG9vbGcQBRBKYXBhbmVzZSBTdHVkaWVzBRBKYXBhbmVzZSBTdHVkaWVzZxAFH0xhbmd1YWdlIFNjaG9vbHMgQWRtaW5pc3RyYXRpb24FH0xhbmd1YWdlIFNjaG9vbHMgQWRtaW5pc3RyYXRpb25nEAUZTGFuZ3VhZ2UgU2Nob29scyBhdCBNaWxscwUZTGFuZ3VhZ2UgU2Nob29scyBhdCBNaWxsc2cQBQdMaWJyYXJ5BQdMaWJyYXJ5ZxAFC01hdGhlbWF0aWNzBQtNYXRoZW1hdGljc2cQBQhNaWRkQ09SRQUITWlkZENPUkVnEAUQTWlkZGxlYnVyeSBpbiBEQwUQTWlkZGxlYnVyeSBpbiBEQ2cQBQ1NdXNldW0gb2YgQXJ0BQ1NdXNldW0gb2YgQXJ0ZxAFBU11c2ljBQVNdXNpY2cQBRJOZXcgRW5nbGFuZCBSZXZpZXcFEk5ldyBFbmdsYW5kIFJldmlld2cQBSVOZXcgRW5nbGFuZCBZb3VuZyBXcml0ZXJzJyBDb25mZXJlbmNlBSVOZXcgRW5nbGFuZCBZb3VuZyBXcml0ZXJzJyBDb25mZXJlbmNlZxAFFU9mZmljZSBvZiBBZHZhbmNlbWVudAUVT2ZmaWNlIG9mIEFkdmFuY2VtZW50ZxAFJVBhcnRvbiBDZW50ZXIgZm9yIEhlYWx0aCBhbmQgV2VsbG5lc3MFJVBhcnRvbiBDZW50ZXIgZm9yIEhlYWx0aCBhbmQgV2VsbG5lc3NnEAUKUGhpbG9zb3BoeQUKUGhpbG9zb3BoeWcQBQdQaHlzaWNzBQdQaHlzaWNzZxAFF1BsYW5uaW5nIGFuZCBBc3Nlc3NtZW50BRdQbGFubmluZyBhbmQgQXNzZXNzbWVudGcQBRFQb2xpdGljYWwgU2NpZW5jZQURUG9saXRpY2FsIFNjaWVuY2VnEAURUG9ydHVndWVzZSBTY2hvb2wFEVBvcnR1Z3Vlc2UgU2Nob29sZxAFElByZXNpZGVudCdzIE9mZmljZQUSUHJlc2lkZW50J3MgT2ZmaWNlZxAFHVByaW50aW5nIGFuZCBNYWlsaW5nIFNlcnZpY2VzBR1QcmludGluZyBhbmQgTWFpbGluZyBTZXJ2aWNlc2cQBSlQcm9ncmFtcyBvbiBDcmVhdGl2aXR5ICYgRW50cmVwcmVuZXVyc2hpcAUpUHJvZ3JhbXMgb24gQ3JlYXRpdml0eSAmIEVudHJlcHJlbmV1cnNoaXBnEAUKUHN5Y2hvbG9neQUKUHN5Y2hvbG9neWcQBQ1QdWJsaWMgU2FmZXR5BQ1QdWJsaWMgU2FmZXR5ZxAFElJlZ2lzdHJhcidzIE9mZmljZQUSUmVnaXN0cmFyJ3MgT2ZmaWNlZxAFCFJlbGlnaW9uBQhSZWxpZ2lvbmcQBRZSZXRhaWwgRm9vZCBPcGVyYXRpb25zBRZSZXRhaWwgRm9vZCBPcGVyYXRpb25zZxAFFFJpa2VydCBOb3JkaWMgQ2VudGVyBRRSaWtlcnQgTm9yZGljIENlbnRlcmcQBSFSb2hhdHluIENlbnRlciBmb3IgR2xvYmFsIEFmZmFpcnMFIVJvaGF0eW4gQ2VudGVyIGZvciBHbG9iYWwgQWZmYWlyc2cQBQdSdXNzaWFuBQdSdXNzaWFuZxAFDlJ1c3NpYW4gU2Nob29sBQ5SdXNzaWFuIFNjaG9vbGcQBRBTY2hvb2wgb2YgS29yZWFuBRBTY2hvb2wgb2YgS29yZWFuZxAFHlNjaWVuY2VzIFRlY2ggU3VwcG9ydCBTZXJ2aWNlcwUeU2NpZW5jZXMgVGVjaCBTdXBwb3J0IFNlcnZpY2VzZxAFClNraSBTY2hvb2wFClNraSBTY2hvb2xnEAUJU25vdyBCb3dsBQlTbm93IEJvd2xnEAUoU25vdyBCb3dsL0ZhY2lsaXRpZXMgU2VydmljZXMtQnJlYWQgTG9hZgUoU25vdyBCb3dsL0ZhY2lsaXRpZXMgU2VydmljZXMtQnJlYWQgTG9hZmcQBRZTb2Npb2xvZ3kvQW50aHJvcG9sb2d5BRZTb2Npb2xvZ3kvQW50aHJvcG9sb2d5ZxAFFlNwYW5pc2ggYW5kIFBvcnR1Z3Vlc2UFFlNwYW5pc2ggYW5kIFBvcnR1Z3Vlc2VnEAUOU3BhbmlzaCBTY2hvb2wFDlNwYW5pc2ggU2Nob29sZxAFHlN0dWRlbnQgQWNjZXNzaWJpbGl0eSBTZXJ2aWNlcwUeU3R1ZGVudCBBY2Nlc3NpYmlsaXR5IFNlcnZpY2VzZxAFKFN0dWRlbnQgRmVsbG93c2hpcHMgJiBIZWFsdGggUHJvZmVzc2lvbnMFKFN0dWRlbnQgRmVsbG93c2hpcHMgJiBIZWFsdGggUHJvZmVzc2lvbnNnEAUaU3R1ZGVudCBGaW5hbmNpYWwgU2VydmljZXMFGlN0dWRlbnQgRmluYW5jaWFsIFNlcnZpY2VzZxAFE1N0dWRlbnQgTWFpbCBDZW50ZXIFE1N0dWRlbnQgTWFpbCBDZW50ZXJnEAUKU3R1ZGlvIEFydAUKU3R1ZGlvIEFydGcQBQdUaGVhdHJlBQdUaGVhdHJlZxAFL1ZpY2UgUHJlc2lkZW50IGZvciBGaW5hbmNlICYgVHJlYXN1cmVyJ3MgT2ZmaWNlBS9WaWNlIFByZXNpZGVudCBmb3IgRmluYW5jZSAmIFRyZWFzdXJlcidzIE9mZmljZWcQBQ9Xcml0aW5nIFByb2dyYW0FD1dyaXRpbmcgUHJvZ3JhbWdkZAIDDw8WAh4HVmlzaWJsZWhkZAIFDzwrAAsBAA8WAh8BaGRkAg0PZBYCZg8WAh8ABZ4fICAgIDxmb290ZXIgaWQ9Im1pZGRfZm9vdGVyIiBjbGFzcz0iZm9vdGVyIj4KICAgICAgPG5hdiBjbGFzcz0iY29udGFpbmVyIj4KICAgICAgICA8dWw+CiAgICAgICAgICA8bGkgY2xhc3M9ImdhdGV3YXlzX3N0dWRlbnRzIj48YSBocmVmPSJodHRwOi8vc3R1ZGVudHMubWlkZGxlYnVyeS5lZHUiPkN1cnJlbnQgU3R1ZGVudHM8c3Bhbj48L3NwYW4+PC9hPjwvbGk+CiAgICAgICAgICA8bGkgY2xhc3M9ImdhdGV3YXlzX3BhcmVudHMiPjxhIGhyZWY9Imh0dHA6Ly9wYXJlbnRzLm1pZGRsZWJ1cnkuZWR1Ij5QYXJlbnRzPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgICAgPGxpIGNsYXNzPSJnYXRld2F5c19zdGFmZiI+PGEgaHJlZj0iaHR0cDovL2ZhY3N0YWZmLm1pZGRsZWJ1cnkuZWR1Ij5GYWN1bHR5ICZhbXA7IFN0YWZmPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgICAgPGxpIGNsYXNzPSJnYXRld2F5c19hbHVtbmkgcXVpY2tfZm9vdGVyIj48YSBocmVmPSJodHRwOi8vYWx1bW5pLm1pZGRsZWJ1cnkuZWR1Ij5BbHVtbmk8c3Bhbj48L3NwYW4+PC9hPgogICAgICAgICAgICA8dWwgY2xhc3M9InF1aWNrX2Zvb3RlciBjb250ZW50cyI+CiAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvYWx1bW5pIj5NaWRkbGVidXJ5IENvbGxlZ2U8L2E+PC9saT4KICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9hbHVtbmkvbHMiPk1pZGRsZWJ1cnkgTGFuZ3VhZ2UgU2Nob29sczwvYT48L2xpPgogICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vd3d3Lm1pZGRsZWJ1cnkuZWR1L2FsdW1uaS9ibHNlIj5NaWRkbGVidXJ5IEJyZWFkIExvYWYgU2Nob29sIG9mIEVuZ2xpc2g8L2E+PC9saT4KICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2FsdW1uaS5taWRkbGVidXJ5LmVkdSI+TWlkZGxlYnVyeSBJbnN0aXR1dGUgb2YgSW50ZXJuYXRpb25hbCBTdHVkaWVzIGF0IE1vbnRlcmV5PC9hPjwvbGk+CiAgICAgICAgICAgIDwvdWw+CiAgICAgICAgICA8L2xpPgogICAgICAgIDwvdWw+CiAgICAgICAgPHVsIGNsYXNzPSJmb290ZXJfcmlnaHQiPgogICAgICAgICAgPGxpIGNsYXNzPSJxdWlja19mb290ZXIgcXVpY2tfZ28iPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdSI+UXVpY2sgTGlua3M8c3Bhbj48L3NwYW4+PC9hPgogICAgICAgICAgICA8ZGl2IGNsYXNzPSJjb250ZW50cyI+CiAgICAgICAgICAgICAgPHVsIGNsYXNzPSJxdWlja19mb290ZXIiPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9iYW5uZXJ3ZWIiPkJhbm5lcldlYjwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS93ZWJtYWlsIj5XZWJtYWlsPC9hPjwvbGk+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L2RpcmVjdG9yeSI+RGlyZWN0b3J5PC9hPjwvbGk+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L2xpYnJhcnkiPkxpYnJhcnk8L2E+PC9saT4KICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vZ28ubWlkZGxlYnVyeS5lZHUvaGVscGRlc2siPlRlY2hub2xvZ3kgSGVscDwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9jYWxlbmRhcj9hY2FkZW1pYyI+QWNhZGVtaWMgQ2FsZW5kYXI8L2E+PC9saT4KICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vZ28ubWlkZGxlYnVyeS5lZHUvd2ViL2Fib3V0Ij5BYm91dCB0aGlzIFNpdGU8L2E+PC9saT4KICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vZ28ubWlkZGxlYnVyeS5lZHUvZXIiPkVtZXJnZW5jeTwvYT48L2xpPgogICAgICAgICAgICAgIDwvdWw+CiAgICAgICAgICAgICAgPHVsIGNsYXNzPSJxdWlja19mb290ZXIiPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9qb2JzZWVrZXJzIj5Kb2IgU2Vla2VyczwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9ib29rc3RvcmUiPkJvb2tzdG9yZTwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9ib3hvZmZpY2UubWlkZGxlYnVyeS5lZHUiPkJveCBPZmZpY2U8L2E+PC9saT4KICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vbXVzZXVtLm1pZGRsZWJ1cnkuZWR1Ij5NdXNldW0gb2YgQXJ0PC9hPjwvbGk+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L3ByZXNpZGVudGlhbC1zZWFyY2giPlByZXNpZGVudGlhbCBTZWFyY2g8L2E+PC9saT4KICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vZ28ubWlkZGxlYnVyeS5lZHUvcHJpdmFjeSI+UHJpdmFjeTwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9jb3B5cmlnaHQiPkNvcHlyaWdodDwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHBzOi8vc2VjdXJlLmV0aGljc3BvaW50LmNvbS9kb21haW4vbWVkaWEvZW4vZ3VpLzI4Mjk2L2luZGV4Lmh0bWwiPkV0aGljc1BvaW50PC9hPjwvbGk+CiAgICAgICAgICAgICAgPC91bD4KICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICA8L2xpPgogICAgICAgICAgPGxpIGNsYXNzPSJxdWlja19mb290ZXIgcXVpY2tfY29udGFjdCI+PGEgaHJlZj0ibWFpbHRvOndlYm1hc3RlckBtaWRkbGVidXJ5LmVkdSI+RGlyZWN0aW9ucyAmYW1wOyBDb250YWN0IEluZm9ybWF0aW9uPHNwYW4+PC9zcGFuPjwvYT4KICAgICAgICAgICAgPGRpdiBjbGFzcz0iY29udGVudHMiPgogICAgICAgICAgICAgIDxwPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9kaXJlY3RvcnkiPkRpcmVjdG9yeTwvYT48L3A+CiAgICAgICAgICAgICAgPHA+CiAgICAgICAgICAgICAgICA8c3Ryb25nPk1haWxpbmcgQWRkcmVzczwvc3Ryb25nPjxicj4KICAgICAgICAgICAgICAgIE1pZGRsZWJ1cnkgQ29sbGVnZTxicj4KICAgICAgICAgICAgICAgIE1pZGRsZWJ1cnksIFZlcm1vbnQgMDU3NTM8YnI+CiAgICAgICAgICAgICAgICA4MDIuNDQzLjUwMDA8YnI+CiAgICAgICAgICAgICAgICA8YSBocmVmPSJodHRwOi8vZ28ubWlkZGxlYnVyeS5lZHUvZGlyZWN0aW9ucyI+RGlyZWN0aW9ucyB0byBNaWRkbGVidXJ5PC9hPgogICAgICAgICAgICAgICAgPGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L3RyYW5zcG9ydGF0aW9uIj5UcmFuc3BvcnRhdGlvbiBPcHRpb25zPC9hPgogICAgICAgICAgICAgIDwvcD4KICAgICAgICAgICAgICA8cD4KICAgICAgICAgICAgICAgIDxzdHJvbmc+QWRtaXNzaW9uczwvc3Ryb25nPiA4MDIuNDQzLjMwMDA8YnI+CiAgICAgICAgICAgICAgICA8YSBocmVmPSJtYWlsdG86YWRtaXNzaW9uc0BtaWRkbGVidXJ5LmVkdSI+YWRtaXNzaW9uc0BtaWRkbGVidXJ5LmVkdTwvYT4KICAgICAgICAgICAgICA8L3A+CiAgICAgICAgICAgICAgPHA+CiAgICAgICAgICAgICAgICA8c3Ryb25nPlB1YmxpYyBTYWZldHk8L3N0cm9uZz4KICAgICAgICAgICAgICAgIDxhIGhyZWY9Im1haWx0bzpwdWJsaWNzYWZldHlAbWlkZGxlYnVyeS5lZHUiPnB1YmxpY3NhZmV0eUBtaWRkbGVidXJ5LmVkdTwvYT4KICAgICAgICAgICAgICA8L3A+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgPC9saT4KICAgICAgICA8L3VsPgogICAgICAgIDxkaXYgY2xhc3M9ImNsZWFyIj48L2Rpdj4KICAgICAgPC9uYXY+CiAgICA8L2Zvb3Rlcj4KICAgIDxkaXYgaWQ9Im1pZGRfZm9vdGVyX3BhbmVsIiBjbGFzcz0iZm9vdGVyX3BhbmVsIj48L2Rpdj5kGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYEBR1jdGwwMCRjdGwwMCRsb2dpblN0YXR1cyRjdGwwMQUdY3RsMDAkY3RsMDAkbG9naW5TdGF0dXMkY3RsMDMFI2N0bDAwJGN0bDAwJExvZ09uJGxvZ2luU3RhdHVzJGN0bDAxBSNjdGwwMCRjdGwwMCRMb2dPbiRsb2dpblN0YXR1cyRjdGwwM7OXB/8/ycdSda66C34YdIQ48Qih',
            '__EVENTVALIDATION': '/wEWiQECge7T9g0CtKjVjQ0CtsCD0wcCpPTp6wICg7qn7gEChoab+QICidnG3QsCidnauAQC3/SBgQYCvvv4xg8CrI/E9gYCtN3ZpwkCk57ApQsClKGerQQCxargsQoCv/LeoQYCsqnOlA8C+KrRqAECrbmt/wUC36Ks0AgCofGEyQECtKqW5wsCzIDrvA8C4sqIhA8Cg4riig4Cpc7WoAMCo8bE0QEC7L2euw0CldzrywQC8aO/lQEC37DRswUCqOfhiwECg+umywYCx9+p0g0CopboyQ8Ctqut2wUC8MnypQIC1tvIxg8CyorlsQECtNqOzAsC74znrQ4CvKH+tgwCtKGKtAkCnueWKQKay9T9BgL5kPzvCQLZ+cbZBQLNqOCqCQKf9sbDAQK/+9iEBwKO0eWyDQKbstukCALPoMizAgKTlLExAsC7lNYCAqPQpd4PAtjYlt4KAviP9s4KAuvHwYcFAvbAzq8HAsyYtd0DAueil4MGAujpyMMJAvntpLoNAsmC05YIApGp59MNApyj0tIPAsqs7YgDAqf8upUNAqzTq4oFAoKYrogMAqbulboHArzG0tQJAo7Pxr4DAvKCwccOAtX746kKAvKutqQHAvv465ELAvL3gpsEAqmv6IQOAvKVicwJAvKG/esMAvHBxMsLAv6MubIJArKSgTgC4b+T5gUC1eScrgMC7v+jqwwCz/6wvQQCmuDq/gQC2uLb5QgCzbGeogUCuJCj8QsCq7rb6QwCyPagmgkC4smGGALc98ViAtW+i/YBAuX29/8GAuqZ3uwBApn58s4OAvWn4IINAoy78egIAvWK6Y4MAoS+gIIJAvDv4LwMAovsvrkKAvHTnogNAuuZ1fEJAtuakGUCvvm8wQUC7r+C1w8C5dKSuAgCgNiEqwYCgsWv5gECza7g/g4C6KLN1QwCpNfykwMCjcKs6ggC2uKp/wICiuuQ8A0Cl6frnQsCwsuO8AMCwMGlGwKtgfbUCQKF9NTUCAK7nK2YBgLdhabDAwLo+oiiBAK/nobgDQLU0bB2Avn+zawNApzN/b4LArKJ+eEMAp6A4vgNAprpsr4LAqSuzJUFwU6VN/HySccQEGfkTKH/8ztx64g=',
            '__VIEWSTATEGENERATOR': 'CA0B0334',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$txtLastName': '',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$txtFirstName': '',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$txtSamaccountname': '',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$txtTelephonenumber': '',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$txtExtensionattribute3': '',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$txtExtensionattribute4': '',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$txtTitle': '',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$ddlType': 'Faculty',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$ddlDepartment': '',
            'ctl00$ctl00$PageContent$PageContent$middDirectoryForm$btnSearch': 'Search'
        }

        profs_r = requests.post("https://directory.middlebury.edu/default.aspx", data=profs_payload)
        profs_soup = BeautifulSoup(profs_r.text)
        profs_results = profs_soup.find_all(class_='ResultItem')

        for result in profs_results:
            contents = result.contents

            # Using str() here raises a UnicodeEncodeError
            # probably because of one department that's a \xa0 (nbsp)
            # instead of a normal space
            name = contents[1].find('a').string.split(', ')
            first_name = name[1].encode('utf-8').strip()
            last_name = name[0].encode('utf-8').strip()

            email = contents[2].find('a').string.encode('utf-8').strip()

            dept = contents[5].string.encode('utf-8').strip()

            # Attempt to normalize the department names using our aliases
            try:
                dept = self.aliases[dept]
            except KeyError:
                pass

            # Only want Middlebury College profs, not MIIS
            if 'miis' not in email and dept not in self.bad_departments:

                # Only create departments that don't already exist
                try:
                    self.prof_dept = Department.objects.get(name=dept)
                except Department.DoesNotExist:
                    self.stdout.write(bcolors.OKBLUE + '  Creating department ' + dept + bcolors.ENDC)
                    self.dept_count += 1
                    self.prof_dept = Department.objects.create(name=dept)

                # Only create professors that don't already exist
                try:
                    Professor.objects.get(email=email)
                except Professor.DoesNotExist:
                    self.stdout.write(bcolors.OKBLUE + '  Creating professor ' +
                                      first_name + " " + last_name + bcolors.ENDC)
                    self.prof_count += 1
                    Professor.objects.create(first=first_name,
                                             last=last_name,
                                             dept=self.prof_dept,
                                             email=email)


        # Scrape the courses
        self.stdout.write(bcolors.HEADER + 'Scraping courses . . .' + bcolors.ENDC)

        # Base url for a department page
        department_base_url = 'https://ssb.middlebury.edu/PNTR/'

        # Url to retrieve all departments
        # Need to append the term, i.e. 201420
        # To get the term, go to the course page and get the url parameter of p_term
        # This should be the first and only argument to scrapecourses
        url = 'https://ssb.middlebury.edu/PNTR/saturn_midd.course_catalog_utlq.catalog_page_by_dept?p_term='

        courses_r = requests.get(url + self.term, verify=False)

        if courses_r.status_code != 200:
            raise CommandError('Unable to retrieve initial course catalog. Status code: %s. URL attempted: %s' % (
                               courses_r.status_code, url + self.term))

        courses_soup = BeautifulSoup(courses_r.text)
        courses_links = courses_soup.find('table').find_all("a")

        for link in courses_links:
            dept = link.string.encode('utf-8')
            self.stdout.write(bcolors.OKBLUE + '  Scraping courses from department ' + dept + bcolors.ENDC)

            course_dept_r = requests.get(department_base_url + link['href'], verify=False)
            course_dept_soup = BeautifulSoup(course_dept_r.text)

            # First table is the departments, first tr is the header
            # We don't want either
            courses_results = course_dept_soup.find_all("table")[1].find_all("tr")[1:]

            # Attempt to normalize the department names using our aliases
            try:
                dept = self.aliases[dept]
            except KeyError:
                pass

            for result in courses_results:
                contents = result.contents

                # First get the title and check it against the list of bad course names
                # We can save a lot of time if we don't want the course
                title = contents[17].string

                if title != None and not any([bad_name in title for bad_name in self.bad_course_names]):
                    title = title.encode('utf-8')

                    try:
                        self.course_dept = Department.objects.get(name=dept)
                    except Department.DoesNotExist:
                        self.stdout.write(bcolors.OKBLUE + '  Creating department ' + dept + bcolors.ENDC)
                        self.dept_count += 1
                        self.course_dept = Department.objects.create(name=dept)

                    # First part is CSCI
                    # Second part is 0302 so int it to drop any leading 0s
                    # then convert back to string to avoid concatenation issues
                    # Third part is section, we don't care about it
                    raw_code = contents[5].string.encode('utf-8').split(" ")
                    dept_code, course_code = raw_code[0], str(int(raw_code[1]))
                    code = dept_code + course_code

                    try:
                        self.course = Course.objects.get(code=code)
                    except Course.DoesNotExist:
                        # Get the crn link to go get the description
                        # First Year Seminars don't have catalog entries
                        # Don't ask me why...
                        crn_link = result.find('a')['href']
                        self.description = get_course_description(crn_link)

                        self.stdout.write(bcolors.OKBLUE + '  Creating course ' + code + bcolors.ENDC)
                        self.course_count += 1
                        self.course = Course.objects.create(code=code,
                                                            title=title,
                                                            description=self.description,
                                                            dept=self.course_dept)

                    # Sometimes there are multiple professors listed separated by ' / '
                    # Only keep the first one
                    instructors = contents[37].string.encode('utf-8').split(' / ')

                    for instructor in instructors:
                        instructor = instructor.split(', ')

                        try:
                            self.instructor_last, self.instructor_first = instructor[0], instructor[1]
                        except IndexError:
                            # Probably means it came up with 'STAFF'
                            # We'll only allow this for Physical Education
                            if dept == 'Physical Education' and instructor == 'STAFF':
                                self.instructor_first = ''
                                self.instructor_last = 'STAFF'

                        try:
                            self.professor = Professor.objects.get(last=self.instructor_last,
                                                                   first__startswith=self.instructor_first)
                        except Professor.MultipleObjectsReturned:
                            self.stdout.write(bcolors.WARNING + '  Warning: multiple professors returned for ' +
                                              self.instructor_last + ' ' + self.instructor_first + bcolors.ENDC)
                            self.stdout.write(bcolors.WARNING + '  Choose a professor for ' + code + bcolors.ENDC)
                            self.professor = pick_professor_interactive(self.instructor_first, self.instructor_last)
                        except Professor.DoesNotExist:
                            self.stdout.write(bcolors.OKBLUE + '  Creating professor ' +
                                              self.instructor_first + ', ' + self.instructor_last + bcolors.ENDC)
                            self.prof_count += 1
                            self.professor = Professor.objects.create(first=self.instructor_first,
                                                                      last=self.instructor_last,
                                                                      dept=self.course_dept)

                        try:
                            ProfCourse.objects.get(prof=self.professor, course=self.course)
                        except ProfCourse.DoesNotExist:
                            self.stdout.write(bcolors.OKBLUE + '  Creating ProfCourse ' +
                                              code + ' ' + self.instructor_last + bcolors.ENDC)
                            self.prof_course_count += 1
                            ProfCourse.objects.create(prof=self.professor, course=self.course)

        self.stdout.write(bcolors.OKGREEN + str(self.prof_count) + ' professors created.' + bcolors.ENDC)
        self.stdout.write(bcolors.OKGREEN + str(self.dept_count) + ' departments created.' + bcolors.ENDC)
        self.stdout.write(bcolors.OKGREEN + str(self.course_count) + ' courses created.' + bcolors.ENDC)
        self.stdout.write(bcolors.OKGREEN + str(self.prof_course_count) + ' prof courses created.' + bcolors.ENDC)

def get_course_description(crn_url):
    """
    Returns the cleaned course description from the associated CRN page.
    """

    base_url = 'https://ssb.middlebury.edu'

    # Follow the first link to the listing page to get the catalog entry
    listing_r = requests.get(base_url + '/PNTR/' + crn_url, verify=False)
    listing_soup = BeautifulSoup(listing_r.text)

    # Follow the catalog link to the catalog entry
    try:
        catalog_url = listing_soup.find('a', text='View Catalog Entry')['href']
        catalog_r = requests.get(base_url + catalog_url, verify=False)
        catalog_soup = BeautifulSoup(catalog_r.text)

        # Get the catalog entry
        catalog_entry = catalog_soup.find('td', class_='ntdefault')
        description = catalog_entry.get_text() \
                                   .encode('utf-8') \
                                   .strip() \
                                   .split('\n')[1]

        return description
    except TypeError:
        # No catalog entry
        return ''

def pick_professor_interactive(first, last):
    choices = Professor.objects.filter(last=last,
                                       first__startswith=first)
    for i, c in enumerate(choices):
        sys.stdout.write('%s  %s. %s %s\n' % (bcolors.WARNING, i + 1, c, bcolors.ENDC))
    choice = raw_input(bcolors.WARNING + '-->' + bcolors.ENDC)
    while int(choice) not in range(1, len(choices) + 1):
        sys.stdout.write(bcolors.WARNING + '  Pick a valid choice.' + bcolors.ENDC)
        choice = raw_input(bcolors.WARNING + '-->' + bcolors.ENDC)
    return choices[int(choice) - 1]

