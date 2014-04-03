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
                        'Chinese School': 'Chinese',
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
                        'German School': 'German',
                        'German/Commons Office - Brainerd': 'German',
                        'Hebrew (Modern)': 'Hebrew',
                        'History of Art & Architecture': 'History of Art and Architecture',
                        'History of Art & Architecture/Arts Center': 'History of Art and Architecture',
                        'Dean of Students/History of Art & Architecture': 'History of Art and Architecture',
                        'International & Global Studies': 'International and Global Studies',
                        'Italian School': 'Italian',
                        'Italian/Commons Office - Cook': 'Italian',
                        'Italian/Italian School': 'Italian',
                        'Japanese Studies': 'Japenese',
                        'Planning and Assessment/Psychology': 'Psychology',
                        'Portuguese School': 'Portuguese',
                        'Religion/Classics': 'Religion',
                        'Religion/Commons Office - Ross': 'Religion',
                        'Russian School': 'Russian',
                        'Spanish School': 'Spanish',
                        u'\xa0': ' '
                        }

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
            '__VIEWSTATE': '/wEPDwUJMzg4Nzc1MDE5D2QWAmYPZBYCZg9kFggCBw9kFgJmDxYCHgRUZXh0BccHICAgIDxoZWFkZXIgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgIDxuYXYgY2xhc3M9ImxlZnRsaW5rcyI+CiAgPGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L21haWwiPldlYk1haWw8L2E+Jm5ic3A7fAogIDxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9idyI+QmFubmVyV2ViPC9hPiZuYnNwO3wKICA8YSBocmVmPSJodHRwOi8vZ28ubWlkZGxlYnVyeS5lZHUvcG9ydGFsIj5Qb3J0YWw8L2E+CjwvbmF2PgogICAgICA8Zm9ybSBjbGFzcz0ic2VhcmNoIiBhY3Rpb249Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvc2VhcmNoIiBtZXRob2Q9ImdldCIgdGFyZ2V0PSJfdG9wIj4KICAgICAgICA8bGFiZWwgZm9yPSJtaWRkX3NlYXJjaF9xdWVyeSI+U2VhcmNoIE1pZGQ8L2xhYmVsPgogICAgICAgIDxpbnB1dCB0eXBlPSJzZWFyY2giIGlkPSJtaWRkX3NlYXJjaF9xdWVyeSIgY2xhc3M9InNlYXJjaF9xdWVyeSB4LXdlYmtpdC1zcGVlY2giIG5hbWU9InEyIiBwbGFjZWhvbGRlcj0iU2VhcmNoIE1pZGQiIHgtd2Via2l0LXNwZWVjaCByZXF1aXJlZD4KICAgICAgICA8aW5wdXQgdHlwZT0ic3VibWl0IiBpZD0ibWlkZF9zZWFyY2hfc3VibWl0IiBjbGFzcz0ic2VhcmNoX3N1Ym1pdCIgdmFsdWU9IkdvIj4KICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBpZD0ibWlkZF9hamF4X3NlYXJjaF91cmwiIHZhbHVlPSJodHRwOi8vd3d3Lm1pZGRsZWJ1cnkuZWR1L2dvL3NlYXJjaCI+CiAgICAgIDwvZm9ybT4KICAgICAgPGgxIGlkPSJtaWRkX3dvcmRtYXJrIiBjbGFzcz0id29yZG1hcmsiPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUiPjxpbWcgc3JjPSIvL2Nkbi5taWRkbGVidXJ5LmVkdS9taWRkbGVidXJ5LmVkdS8yMDEwL2ltYWdlcy9sb2dvLnBuZyIgd2lkdGg9IjIwNiIgaGVpZ2h0PSIzOSIgYWx0PSJNaWRkbGVidXJ5Ij48L2E+PC9oMT4KICAgIDwvaGVhZGVyPmQCCQ9kFgJmDxYCHwAF2wwgICAgPG5hdiBpZD0ibWlkZF9uYXZpZ2F0aW9uIiBjbGFzcz0ibmF2aWdhdGlvbiBjb250YWluZXIiPgogICAgICA8dWw+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfYWRtaXNzaW9ucyB0b3AiPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvYWRtaXNzaW9ucyI+QWRtaXNzaW9uczxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICA8bGkgY2xhc3M9Im5hdl9hY2FkZW1pY3MgdG9wIj48YSBocmVmPSJodHRwOi8vd3d3Lm1pZGRsZWJ1cnkuZWR1L2FjYWRlbWljcyI+QWNhZGVtaWNzPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2X3N0dWRlbnRsaWZlIHRvcCI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9zdHVkZW50bGlmZSI+U3R1ZGVudCBMaWZlPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2X2F0aGxldGljcyB0b3AiPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvYXRobGV0aWNzIj5BdGhsZXRpY3M8c3Bhbj48L3NwYW4+PC9hPjwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfYXJ0cyB0b3AiPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvYXJ0cyI+QXJ0czxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICA8bGkgY2xhc3M9Im5hdl9pbnRlcm5hdGlvbmFsIHRvcCI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9pbnRlcm5hdGlvbmFsIj5NaWRkbGVidXJ5IEludGVybmF0aW9uYWw8c3Bhbj48L3NwYW4+PC9hPjwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfbWlkZGxhYiB0b3AiPjxhIGhyZWY9Imh0dHA6Ly9taWRkbGFiLm1pZGRsZWJ1cnkuZWR1LyI+TWlkZExhYjxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICA8bGkgY2xhc3M9Im5hdl9hYm91dCBib3R0b20iPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvYWJvdXQiPkFib3V0PHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2X3N1c3RhaW5hYmlsaXR5IGJvdHRvbSI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9zdXN0YWluYWJpbGl0eSI+U3VzdGFpbmFiaWxpdHk8c3Bhbj48L3NwYW4+PC9hPjwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfZ2l2aW5nIGJvdHRvbSI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9naXZpbmciPkdpdmluZzxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICA8bGkgY2xhc3M9Im5hdl9uZXdzIGJvdHRvbSI+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9uZXdzcm9vbSI+TmV3cyBSb29tPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2X2V2ZW50cyBib3R0b20iPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvZXZlbnRzIj5DYWxlbmRhciBvZiBFdmVudHM8c3Bhbj48L3NwYW4+PC9hPjwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXZfb2ZmaWNlcyBib3R0b20iPjxhIGhyZWY9Imh0dHA6Ly93d3cubWlkZGxlYnVyeS5lZHUvb2ZmaWNlcyI+T2ZmaWNlICZhbXA7IFNlcnZpY2VzPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICA8L3VsPgogICAgPC9uYXY+ZAILD2QWAgIBD2QWAgIDD2QWAmYPZBYGAgEPZBYCAhsPEGQPFoIBZgIBAgICAwIEAgUCBgIHAggCCQIKAgsCDAINAg4CDwIQAhECEgITAhQCFQIWAhcCGAIZAhoCGwIcAh0CHgIfAiACIQIiAiMCJAIlAiYCJwIoAikCKgIrAiwCLQIuAi8CMAIxAjICMwI0AjUCNgI3AjgCOQI6AjsCPAI9Aj4CPwJAAkECQgJDAkQCRQJGAkcCSAJJAkoCSwJMAk0CTgJPAlACUQJSAlMCVAJVAlYCVwJYAlkCWgJbAlwCXQJeAl8CYAJhAmICYwJkAmUCZgJnAmgCaQJqAmsCbAJtAm4CbwJwAnECcgJzAnQCdQJ2AncCeAJ5AnoCewJ8An0CfgJ/AoABAoEBFoIBEAUOQW55IERlcGFydG1lbnRlZxAFEEFjYWRlbWljIEFmZmFpcnMFEEFjYWRlbWljIEFmZmFpcnNnEAUuQWNhZGVtaWMgQWZmYWlycy9HZW5kZXIsIFNleHVhbGl0eS9GZW0gU3R1ZGllcwUuQWNhZGVtaWMgQWZmYWlycy9HZW5kZXIsIFNleHVhbGl0eS9GZW0gU3R1ZGllc2cQBQpBZG1pc3Npb25zBQpBZG1pc3Npb25zZxAFI0FkbWlzc2lvbnMvQ29tbW9ucyBPZmZpY2UgLSBBdHdhdGVyBSNBZG1pc3Npb25zL0NvbW1vbnMgT2ZmaWNlIC0gQXR3YXRlcmcQBRBBbWVyaWNhbiBTdHVkaWVzBRBBbWVyaWNhbiBTdHVkaWVzZxAFBkFyYWJpYwUGQXJhYmljZxAFC0FydHMgQ2VudGVyBQtBcnRzIENlbnRlcmcQBRxBc3Npc3RhbnQgVHJlYXN1cmVyJ3MgT2ZmaWNlBRxBc3Npc3RhbnQgVHJlYXN1cmVyJ3MgT2ZmaWNlZxAFCUF0aGxldGljcwUJQXRobGV0aWNzZxAFGUF0aGxldGljcy9EaW5pbmcgU2VydmljZXMFGUF0aGxldGljcy9EaW5pbmcgU2VydmljZXNnEAUTQXRobGV0aWNzL1Nub3cgQm93bAUTQXRobGV0aWNzL1Nub3cgQm93bGcQBQdCaW9sb2d5BQdCaW9sb2d5ZxAFHEJyZWFkIExvYWYgU2Nob29sIG9mIEVuZ2xpc2gFHEJyZWFkIExvYWYgU2Nob29sIG9mIEVuZ2xpc2hnEAUeQnJlYWQgTG9hZiBXcml0ZXJzJyBDb25mZXJlbmNlBR5CcmVhZCBMb2FmIFdyaXRlcnMnIENvbmZlcmVuY2VnEAUNQnVkZ2V0IE9mZmljZQUNQnVkZ2V0IE9mZmljZWcQBQ9CdXNpbmVzcyBPZmZpY2UFD0J1c2luZXNzIE9mZmljZWcQBSxDZW50ZXIgQ29tcGFyYXRpdmUgU3R1ZHkgb2YgUmFjZSAmIEV0aG5pY2l0eQUsQ2VudGVyIENvbXBhcmF0aXZlIFN0dWR5IG9mIFJhY2UgJiBFdGhuaWNpdHlnEAUiQ2VudGVyIGZvciBDYXJlZXJzIGFuZCBJbnRlcm5zaGlwcwUiQ2VudGVyIGZvciBDYXJlZXJzIGFuZCBJbnRlcm5zaGlwc2cQBSVDZW50ZXIgZm9yIENvdW5zZWxpbmcvSHVtYW4gUmVsYXRpb25zBSVDZW50ZXIgZm9yIENvdW5zZWxpbmcvSHVtYW4gUmVsYXRpb25zZxAFJUNlbnRlciBmb3IgVGVhY2hpbmcvTGVhcm5pbmcvUmVzZWFyY2gFJUNlbnRlciBmb3IgVGVhY2hpbmcvTGVhcm5pbmcvUmVzZWFyY2hnEAURQ2hhcGxhaW4ncyBPZmZpY2UFEUNoYXBsYWluJ3MgT2ZmaWNlZxAFGkNoZW1pc3RyeSBhbmQgQmlvY2hlbWlzdHJ5BRpDaGVtaXN0cnkgYW5kIEJpb2NoZW1pc3RyeWcQBQdDaGluZXNlBQdDaGluZXNlZxAFDkNoaW5lc2UgU2Nob29sBQ5DaGluZXNlIFNjaG9vbGcQBQhDbGFzc2ljcwUIQ2xhc3NpY3NnEAUTQ29sbGVnZSBBZHZhbmNlbWVudAUTQ29sbGVnZSBBZHZhbmNlbWVudGcQBQ1Db2xsZWdlIFN0b3JlBQ1Db2xsZWdlIFN0b3JlZxAFGENvbW1vbnMgT2ZmaWNlIC0gQXR3YXRlcgUYQ29tbW9ucyBPZmZpY2UgLSBBdHdhdGVyZxAFGUNvbW1vbnMgT2ZmaWNlIC0gQnJhaW5lcmQFGUNvbW1vbnMgT2ZmaWNlIC0gQnJhaW5lcmRnEAUVQ29tbW9ucyBPZmZpY2UgLSBDb29rBRVDb21tb25zIE9mZmljZSAtIENvb2tnEAUVQ29tbW9ucyBPZmZpY2UgLSBSb3NzBRVDb21tb25zIE9mZmljZSAtIFJvc3NnEAUaQ29tbW9ucyBPZmZpY2UgLSBXb25uYWNvdHQFGkNvbW1vbnMgT2ZmaWNlIC0gV29ubmFjb3R0ZxAFDkNvbW11bmljYXRpb25zBQ5Db21tdW5pY2F0aW9uc2cQBRRDb21tdW5pdHkgRW5nYWdlbWVudAUUQ29tbXVuaXR5IEVuZ2FnZW1lbnRnEAUQQ29tcHV0ZXIgU2NpZW5jZQUQQ29tcHV0ZXIgU2NpZW5jZWcQBRNDb250cm9sbGVyJ3MgT2ZmaWNlBRNDb250cm9sbGVyJ3MgT2ZmaWNlZxAFF0NyZWF0aXZpdHkgJiBJbm5vdmF0aW9uBRdDcmVhdGl2aXR5ICYgSW5ub3ZhdGlvbmcQBS1DdHIgZm9yIENhbXB1cyBBY3Rpdml0aWVzICYgTGVhZGVyc2hpcCAoQ0NBTCkFLUN0ciBmb3IgQ2FtcHVzIEFjdGl2aXRpZXMgJiBMZWFkZXJzaGlwIChDQ0FMKWcQBQVEYW5jZQUFRGFuY2VnEAUjRGFuY2UvSGlzdG9yeSBvZiBBcnQgJiBBcmNoaXRlY3R1cmUFI0RhbmNlL0hpc3Rvcnkgb2YgQXJ0ICYgQXJjaGl0ZWN0dXJlZxAFK0RhdmlzIFVuaXRlZCBXb3JsZCBDb2xsZWdlIFNjaG9sYXJzIFByb2dyYW0FK0RhdmlzIFVuaXRlZCBXb3JsZCBDb2xsZWdlIFNjaG9sYXJzIFByb2dyYW1nEAUYRGVhbiBvZiBGYWN1bHR5J3MgT2ZmaWNlBRhEZWFuIG9mIEZhY3VsdHkncyBPZmZpY2VnEAUQRGVhbiBvZiBTdHVkZW50cwUQRGVhbiBvZiBTdHVkZW50c2cQBS9EZWFuIG9mIFN0dWRlbnRzL0NlbnRlciBmb3IgRWR1Y2F0aW9uIGluIEFjdGlvbgUvRGVhbiBvZiBTdHVkZW50cy9DZW50ZXIgZm9yIEVkdWNhdGlvbiBpbiBBY3Rpb25nEAUuRGVhbiBvZiBTdHVkZW50cy9IaXN0b3J5IG9mIEFydCAmIEFyY2hpdGVjdHVyZQUuRGVhbiBvZiBTdHVkZW50cy9IaXN0b3J5IG9mIEFydCAmIEFyY2hpdGVjdHVyZWcQBRNEZWFuIG9mIHRoZSBDb2xsZWdlBRNEZWFuIG9mIHRoZSBDb2xsZWdlZxAFD0RpbmluZyBTZXJ2aWNlcwUPRGluaW5nIFNlcnZpY2VzZxAFCUVjb25vbWljcwUJRWNvbm9taWNzZxAFIUVjb25vbWljcy9DcmVhdGl2aXR5ICYgSW5ub3ZhdGlvbgUhRWNvbm9taWNzL0NyZWF0aXZpdHkgJiBJbm5vdmF0aW9uZxAFEUVkdWNhdGlvbiBTdHVkaWVzBRFFZHVjYXRpb24gU3R1ZGllc2cQBSxFZHVjYXRpb24gU3R1ZGllcy9Db21tb25zIE9mZmljZSAtIFdvbm5hY290dAUsRWR1Y2F0aW9uIFN0dWRpZXMvQ29tbW9ucyBPZmZpY2UgLSBXb25uYWNvdHRnEAUuRUlBOiBDYXJlZXJzLCBGZWxsb3dzaGlwcyBhbmQgQ2l2aWMgRW5nYWdlbWVudAUuRUlBOiBDYXJlZXJzLCBGZWxsb3dzaGlwcyBhbmQgQ2l2aWMgRW5nYWdlbWVudGcQBR5FbmdsaXNoICYgQW1lcmljYW4gTGl0ZXJhdHVyZXMFHkVuZ2xpc2ggJiBBbWVyaWNhbiBMaXRlcmF0dXJlc2cQBRVFbnZpcm9ubWVudGFsIEFmZmFpcnMFFUVudmlyb25tZW50YWwgQWZmYWlyc2cQBRVFbnZpcm9ubWVudGFsIFN0dWRpZXMFFUVudmlyb25tZW50YWwgU3R1ZGllc2cQBR1FbnZpcm9ubWVudGFsIFN0dWRpZXMvQmlvbG9neQUdRW52aXJvbm1lbnRhbCBTdHVkaWVzL0Jpb2xvZ3lnEAUdRW52aXJvbm1lbnRhbCBTdHVkaWVzL0hpc3RvcnkFHUVudmlyb25tZW50YWwgU3R1ZGllcy9IaXN0b3J5ZxAFEUV2ZW50cyBNYW5hZ2VtZW50BRFFdmVudHMgTWFuYWdlbWVudGcQBRNGYWNpbGl0aWVzIFNlcnZpY2VzBRNGYWNpbGl0aWVzIFNlcnZpY2VzZxAFIEZhY2lsaXRpZXMgU2VydmljZXMgLSBCcmVhZCBMb2FmBSBGYWNpbGl0aWVzIFNlcnZpY2VzIC0gQnJlYWQgTG9hZmcQBRZGaWxtIGFuZCBNZWRpYSBDdWx0dXJlBRZGaWxtIGFuZCBNZWRpYSBDdWx0dXJlZxAFBkZyZW5jaAUGRnJlbmNoZxAFJEdlbmRlciwgU2V4dWFsaXR5ICYgRmVtaW5pc3QgU3R1ZGllcwUkR2VuZGVyLCBTZXh1YWxpdHkgJiBGZW1pbmlzdCBTdHVkaWVzZxAFCUdlb2dyYXBoeQUJR2VvZ3JhcGh5ZxAFIkdlb2dyYXBoeS9Db21tb25zIE9mZmljZSAtIEF0d2F0ZXIFIkdlb2dyYXBoeS9Db21tb25zIE9mZmljZSAtIEF0d2F0ZXJnEAUHR2VvbG9neQUHR2VvbG9neWcQBQZHZXJtYW4FBkdlcm1hbmcQBQ1HZXJtYW4gU2Nob29sBQ1HZXJtYW4gU2Nob29sZxAFIEdlcm1hbi9Db21tb25zIE9mZmljZSAtIEJyYWluZXJkBSBHZXJtYW4vQ29tbW9ucyBPZmZpY2UgLSBCcmFpbmVyZGcQBQtHb2xmIENvdXJzZQULR29sZiBDb3Vyc2VnEAUtSEFUQyBJbnN0aXR1dGUgZm9yIEFkdmFuY2VtZW50IG9mIEhlYnJldyBMYW5nBS1IQVRDIEluc3RpdHV0ZSBmb3IgQWR2YW5jZW1lbnQgb2YgSGVicmV3IExhbmdnEAUHSGlzdG9yeQUHSGlzdG9yeWcQBR1IaXN0b3J5IG9mIEFydCAmIEFyY2hpdGVjdHVyZQUdSGlzdG9yeSBvZiBBcnQgJiBBcmNoaXRlY3R1cmVnEAUPSHVtYW4gUmVzb3VyY2VzBQ9IdW1hbiBSZXNvdXJjZXNnEAUKSHVtYW5pdGllcwUKSHVtYW5pdGllc2cQBR5JbnRlcm5hdGlvbmFsICYgR2xvYmFsIFN0dWRpZXMFHkludGVybmF0aW9uYWwgJiBHbG9iYWwgU3R1ZGllc2cQBSlJbnRlcm5hdGlvbmFsIFByb2dyYW1zICYgT2ZmLUNhbXB1cyBTdHVkeQUpSW50ZXJuYXRpb25hbCBQcm9ncmFtcyAmIE9mZi1DYW1wdXMgU3R1ZHlnEAUoSW50ZXJuYXRpb25hbCBTdHVkZW50ICYgU2Nob2xhciBTZXJ2aWNlcwUoSW50ZXJuYXRpb25hbCBTdHVkZW50ICYgU2Nob2xhciBTZXJ2aWNlc2cQBQdJdGFsaWFuBQdJdGFsaWFuZxAFDkl0YWxpYW4gU2Nob29sBQ5JdGFsaWFuIFNjaG9vbGcQBRBKYXBhbmVzZSBTdHVkaWVzBRBKYXBhbmVzZSBTdHVkaWVzZxAFH0xhbmd1YWdlIFNjaG9vbHMgQWRtaW5pc3RyYXRpb24FH0xhbmd1YWdlIFNjaG9vbHMgQWRtaW5pc3RyYXRpb25nEAUZTGFuZ3VhZ2UgU2Nob29scyBhdCBNaWxscwUZTGFuZ3VhZ2UgU2Nob29scyBhdCBNaWxsc2cQBR5MaWJyYXJ5ICYgSW5mb3JtYXRpb24gU2VydmljZXMFHkxpYnJhcnkgJiBJbmZvcm1hdGlvbiBTZXJ2aWNlc2cQBQ9NYWlsaW5nIFNlcnZpY2UFD01haWxpbmcgU2VydmljZWcQBQtNYXRoZW1hdGljcwULTWF0aGVtYXRpY3NnEAUQTWlkZGxlYnVyeSBpbiBEQwUQTWlkZGxlYnVyeSBpbiBEQ2cQBQ1NdXNldW0gb2YgQXJ0BQ1NdXNldW0gb2YgQXJ0ZxAFBU11c2ljBQVNdXNpY2cQBRJOZXcgRW5nbGFuZCBSZXZpZXcFEk5ldyBFbmdsYW5kIFJldmlld2cQBS1OZXcgRW5nbGFuZCBSZXZpZXcvTGlicmFyeSBhbmQgSW5mby4gU2VydmljZXMFLU5ldyBFbmdsYW5kIFJldmlldy9MaWJyYXJ5IGFuZCBJbmZvLiBTZXJ2aWNlc2cQBSJOZXcgRW5nbGFuZCBSZXZpZXcvV3JpdGluZyBQcm9ncmFtBSJOZXcgRW5nbGFuZCBSZXZpZXcvV3JpdGluZyBQcm9ncmFtZxAFJU5ldyBFbmdsYW5kIFlvdW5nIFdyaXRlcnMnIENvbmZlcmVuY2UFJU5ldyBFbmdsYW5kIFlvdW5nIFdyaXRlcnMnIENvbmZlcmVuY2VnEAUlUGFydG9uIENlbnRlciBmb3IgSGVhbHRoIGFuZCBXZWxsbmVzcwUlUGFydG9uIENlbnRlciBmb3IgSGVhbHRoIGFuZCBXZWxsbmVzc2cQBQpQaGlsb3NvcGh5BQpQaGlsb3NvcGh5ZxAFB1BoeXNpY3MFB1BoeXNpY3NnEAUXUGxhbm5pbmcgYW5kIEFzc2Vzc21lbnQFF1BsYW5uaW5nIGFuZCBBc3Nlc3NtZW50ZxAFIlBsYW5uaW5nIGFuZCBBc3Nlc3NtZW50L1BzeWNob2xvZ3kFIlBsYW5uaW5nIGFuZCBBc3Nlc3NtZW50L1BzeWNob2xvZ3lnEAURUG9saXRpY2FsIFNjaWVuY2UFEVBvbGl0aWNhbCBTY2llbmNlZxAFEVBvcnR1Z3Vlc2UgU2Nob29sBRFQb3J0dWd1ZXNlIFNjaG9vbGcQBRJQcmVzaWRlbnQncyBPZmZpY2UFElByZXNpZGVudCdzIE9mZmljZWcQBQpQc3ljaG9sb2d5BQpQc3ljaG9sb2d5ZxAFIlBzeWNob2xvZ3kvUGxhbm5pbmcgYW5kIEFzc2Vzc21lbnQFIlBzeWNob2xvZ3kvUGxhbm5pbmcgYW5kIEFzc2Vzc21lbnRnEAUNUHVibGljIFNhZmV0eQUNUHVibGljIFNhZmV0eWcQBRJSZWdpc3RyYXIncyBPZmZpY2UFElJlZ2lzdHJhcidzIE9mZmljZWcQBSpSZWdpc3RyYXIncyBPZmZpY2UvUGxhbm5pbmcgYW5kIEFzc2Vzc21lbnQFKlJlZ2lzdHJhcidzIE9mZmljZS9QbGFubmluZyBhbmQgQXNzZXNzbWVudGcQBQhSZWxpZ2lvbgUIUmVsaWdpb25nEAUeUmVsaWdpb24vQ29tbW9ucyBPZmZpY2UgLSBSb3NzBR5SZWxpZ2lvbi9Db21tb25zIE9mZmljZSAtIFJvc3NnEAUNUmVwcm9ncmFwaGljcwUNUmVwcm9ncmFwaGljc2cQBRZSZXRhaWwgRm9vZCBPcGVyYXRpb25zBRZSZXRhaWwgRm9vZCBPcGVyYXRpb25zZxAFFFJpa2VydCBOb3JkaWMgQ2VudGVyBRRSaWtlcnQgTm9yZGljIENlbnRlcmcQBSFSb2hhdHluIENlbnRlciBmb3IgR2xvYmFsIEFmZmFpcnMFIVJvaGF0eW4gQ2VudGVyIGZvciBHbG9iYWwgQWZmYWlyc2cQBQdSdXNzaWFuBQdSdXNzaWFuZxAFDlJ1c3NpYW4gU2Nob29sBQ5SdXNzaWFuIFNjaG9vbGcQBRBTY2hvb2wgb2YgSGVicmV3BRBTY2hvb2wgb2YgSGVicmV3ZxAFHlNjaWVuY2VzIFRlY2ggU3VwcG9ydCBTZXJ2aWNlcwUeU2NpZW5jZXMgVGVjaCBTdXBwb3J0IFNlcnZpY2VzZxAFClNraSBTY2hvb2wFClNraSBTY2hvb2xnEAUJU25vdyBCb3dsBQlTbm93IEJvd2xnEAUWU29jaW9sb2d5L0FudGhyb3BvbG9neQUWU29jaW9sb2d5L0FudGhyb3BvbG9neWcQBRZTcGFuaXNoIGFuZCBQb3J0dWd1ZXNlBRZTcGFuaXNoIGFuZCBQb3J0dWd1ZXNlZxAFDlNwYW5pc2ggU2Nob29sBQ5TcGFuaXNoIFNjaG9vbGcQBR5TdHVkZW50IEFjY2Vzc2liaWxpdHkgU2VydmljZXMFHlN0dWRlbnQgQWNjZXNzaWJpbGl0eSBTZXJ2aWNlc2cQBShTdHVkZW50IEZlbGxvd3NoaXBzICYgSGVhbHRoIFByb2Zlc3Npb25zBShTdHVkZW50IEZlbGxvd3NoaXBzICYgSGVhbHRoIFByb2Zlc3Npb25zZxAFGlN0dWRlbnQgRmluYW5jaWFsIFNlcnZpY2VzBRpTdHVkZW50IEZpbmFuY2lhbCBTZXJ2aWNlc2cQBRNTdHVkZW50IE1haWwgQ2VudGVyBRNTdHVkZW50IE1haWwgQ2VudGVyZxAFClN0dWRpbyBBcnQFClN0dWRpbyBBcnRnEAUHVGhlYXRyZQUHVGhlYXRyZWcQBS9WaWNlIFByZXNpZGVudCBmb3IgRmluYW5jZSAmIFRyZWFzdXJlcidzIE9mZmljZQUvVmljZSBQcmVzaWRlbnQgZm9yIEZpbmFuY2UgJiBUcmVhc3VyZXIncyBPZmZpY2VnEAUPV3JpdGluZyBQcm9ncmFtBQ9Xcml0aW5nIFByb2dyYW1nZGQCAw8PFgIeB1Zpc2libGVoZGQCBQ88KwALAQAPFgIfAWhkZAIND2QWAmYPFgIfAAXuHSAgICA8Zm9vdGVyIGlkPSJtaWRkX2Zvb3RlciIgY2xhc3M9ImZvb3RlciI+CiAgICAgIDxuYXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgICAgPHVsPgogICAgICAgICAgPGxpIGNsYXNzPSJnYXRld2F5c19zdHVkZW50cyI+PGEgaHJlZj0iaHR0cDovL3N0dWRlbnRzLm1pZGRsZWJ1cnkuZWR1Ij5DdXJyZW50IFN0dWRlbnRzPHNwYW4+PC9zcGFuPjwvYT48L2xpPgogICAgICAgICAgPGxpIGNsYXNzPSJnYXRld2F5c19wYXJlbnRzIj48YSBocmVmPSJodHRwOi8vcGFyZW50cy5taWRkbGVidXJ5LmVkdSI+UGFyZW50czxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICAgIDxsaSBjbGFzcz0iZ2F0ZXdheXNfc3RhZmYiPjxhIGhyZWY9Imh0dHA6Ly9mYWNzdGFmZi5taWRkbGVidXJ5LmVkdSI+RmFjdWx0eSAmYW1wOyBTdGFmZjxzcGFuPjwvc3Bhbj48L2E+PC9saT4KICAgICAgICAgIDxsaSBjbGFzcz0iZ2F0ZXdheXNfYWx1bW5pIHF1aWNrX2Zvb3RlciI+PGEgaHJlZj0iaHR0cDovL2FsdW1uaS5taWRkbGVidXJ5LmVkdSI+QWx1bW5pPHNwYW4+PC9zcGFuPjwvYT4KICAgICAgICAgICAgPHVsIGNsYXNzPSJxdWlja19mb290ZXIgY29udGVudHMiPgogICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vd3d3Lm1pZGRsZWJ1cnkuZWR1L2FsdW1uaSI+VW5kZXJncmFkdWF0ZSBBbHVtbmk8L2E+PC9saT4KICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9hbHVtbmkvbHMiPkxhbmd1YWdlIFNjaG9vbHM8L2E+PC9saT4KICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL3d3dy5taWRkbGVidXJ5LmVkdS9hbHVtbmkvYmxzZSI+QnJlYWQgTG9hZiBTY2hvb2wgb2YgRW5nbGlzaDwvYT48L2xpPgogICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vYWx1bW5pLm1paXMuZWR1Ij5Nb250ZXJleSBJbnN0aXR1dGU8L2E+PC9saT4KICAgICAgICAgICAgPC91bD4KICAgICAgICAgIDwvbGk+CiAgICAgICAgPC91bD4KICAgICAgICA8dWwgY2xhc3M9ImZvb3Rlcl9yaWdodCI+CiAgICAgICAgICA8bGkgY2xhc3M9InF1aWNrX2Zvb3RlciBxdWlja19nbyI+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1Ij5RdWljayBMaW5rczxzcGFuPjwvc3Bhbj48L2E+CiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImNvbnRlbnRzIj4KICAgICAgICAgICAgICA8dWwgY2xhc3M9InF1aWNrX2Zvb3RlciI+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L2Jhbm5lcndlYiI+QmFubmVyV2ViPC9hPjwvbGk+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L3dlYm1haWwiPldlYm1haWw8L2E+PC9saT4KICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vZ28ubWlkZGxlYnVyeS5lZHUvZGlyZWN0b3J5Ij5EaXJlY3Rvcnk8L2E+PC9saT4KICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vZ28ubWlkZGxlYnVyeS5lZHUvbGlicmFyeSI+TGlicmFyeTwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9oZWxwZGVzayI+VGVjaG5vbG9neSBIZWxwPC9hPjwvbGk+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L2NhbGVuZGFyP2FjYWRlbWljIj5BY2FkZW1pYyBDYWxlbmRhcjwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS93ZWIvYWJvdXQiPkFib3V0IHRoaXMgU2l0ZTwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9lciI+RW1lcmdlbmN5PC9hPjwvbGk+CiAgICAgICAgICAgICAgPC91bD4KICAgICAgICAgICAgICA8dWwgY2xhc3M9InF1aWNrX2Zvb3RlciI+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L2pvYnNlZWtlcnMiPkpvYiBTZWVrZXJzPC9hPjwvbGk+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L2Jvb2tzdG9yZSI+Qm9va3N0b3JlPC9hPjwvbGk+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2JveG9mZmljZS5taWRkbGVidXJ5LmVkdSI+Qm94IE9mZmljZTwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9tdXNldW0ubWlkZGxlYnVyeS5lZHUiPk11c2V1bSBvZiBBcnQ8L2E+PC9saT4KICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwOi8vZ28ubWlkZGxlYnVyeS5lZHUvY2FtcHVzbWFwIj5DYW1wdXMgTWFwczwvYT48L2xpPgogICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9wcml2YWN5Ij5Qcml2YWN5PC9hPjwvbGk+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L2NvcHlyaWdodCI+Q29weXJpZ2h0PC9hPjwvbGk+CiAgICAgICAgICAgICAgICA8bGk+PGEgaHJlZj0iaHR0cHM6Ly9zZWN1cmUuZXRoaWNzcG9pbnQuY29tL2RvbWFpbi9tZWRpYS9lbi9ndWkvMjgyOTYvaW5kZXguaHRtbCI+RXRoaWNzUG9pbnQ8L2E+PC9saT4KICAgICAgICAgICAgICA8L3VsPgogICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgIDwvbGk+CiAgICAgICAgICA8bGkgY2xhc3M9InF1aWNrX2Zvb3RlciBxdWlja19jb250YWN0Ij48YSBocmVmPSJtYWlsdG86d2VibWFzdGVyQG1pZGRsZWJ1cnkuZWR1Ij5EaXJlY3Rpb25zICZhbXA7IENvbnRhY3QgSW5mb3JtYXRpb248c3Bhbj48L3NwYW4+PC9hPgogICAgICAgICAgICA8ZGl2IGNsYXNzPSJjb250ZW50cyI+CiAgICAgICAgICAgICAgPHA+PGEgaHJlZj0iaHR0cDovL2dvLm1pZGRsZWJ1cnkuZWR1L2RpcmVjdG9yeSI+RGlyZWN0b3J5PC9hPjwvcD4KICAgICAgICAgICAgICA8cD4KICAgICAgICAgICAgICAgIDxzdHJvbmc+TWFpbGluZyBBZGRyZXNzPC9zdHJvbmc+PGJyPgogICAgICAgICAgICAgICAgTWlkZGxlYnVyeSBDb2xsZWdlPGJyPgogICAgICAgICAgICAgICAgTWlkZGxlYnVyeSwgVmVybW9udCAwNTc1Mzxicj4KICAgICAgICAgICAgICAgIDgwMi40NDMuNTAwMDxicj4KICAgICAgICAgICAgICAgIDxhIGhyZWY9Imh0dHA6Ly9nby5taWRkbGVidXJ5LmVkdS9kaXJlY3Rpb25zIj5EaXJlY3Rpb25zIHRvIE1pZGRsZWJ1cnk8L2E+CiAgICAgICAgICAgICAgPC9wPgogICAgICAgICAgICAgIDxwPgogICAgICAgICAgICAgICAgPHN0cm9uZz5BZG1pc3Npb25zPC9zdHJvbmc+IDgwMi40NDMuMzAwMDxicj4KICAgICAgICAgICAgICAgIDxhIGhyZWY9Im1haWx0bzphZG1pc3Npb25zQG1pZGRsZWJ1cnkuZWR1Ij5hZG1pc3Npb25zQG1pZGRsZWJ1cnkuZWR1PC9hPgogICAgICAgICAgICAgIDwvcD4KICAgICAgICAgICAgICA8cD4KICAgICAgICAgICAgICAgIDxzdHJvbmc+UHVibGljIFNhZmV0eTwvc3Ryb25nPgogICAgICAgICAgICAgICAgPGEgaHJlZj0ibWFpbHRvOnB1YmxpY3NhZmV0eUBtaWRkbGVidXJ5LmVkdSI+cHVibGljc2FmZXR5QG1pZGRsZWJ1cnkuZWR1PC9hPgogICAgICAgICAgICAgIDwvcD4KICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICA8L2xpPgogICAgICAgIDwvdWw+CiAgICAgICAgPGRpdiBjbGFzcz0iY2xlYXIiPjwvZGl2PgogICAgICA8L25hdj4KICAgIDwvZm9vdGVyPgogICAgPGRpdiBpZD0ibWlkZF9mb290ZXJfcGFuZWwiIGNsYXNzPSJmb290ZXJfcGFuZWwiPjwvZGl2PmQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgQFHWN0bDAwJGN0bDAwJGxvZ2luU3RhdHVzJGN0bDAxBR1jdGwwMCRjdGwwMCRsb2dpblN0YXR1cyRjdGwwMwUjY3RsMDAkY3RsMDAkTG9nT24kbG9naW5TdGF0dXMkY3RsMDEFI2N0bDAwJGN0bDAwJExvZ09uJGxvZ2luU3RhdHVzJGN0bDAzwne+Be4mqzD+NMXA74AiyYzMKUI=',
            '__EVENTVALIDATION': '/wEWlAECq5vXnwYCtKjVjQ0CtsCD0wcCpPTp6wICg7qn7gEChoab+QICidnG3QsCidnauAQC3/SBgQYCvvv4xg8CrI/E9gYCtN3ZpwkCk57ApQsClKGerQQCxargsQoCv/LeoQYCsqnOlA8C+KrRqAECnvuW8g0Crbmt/wUCg/qBtAMC36Ks0AgCofGEyQECtKqW5wsCzIDrvA8C4sqIhA8Cl/WenQEC4JPFnw0Cpc7WoAMCo8bE0QEC7L2euw0CldzrywQC8aO/lQEC4t//3Q0C37DRswUCqOfhiwECg+umywYCx9+p0g0CopboyQ8Ctqut2wUC8MnypQIC1tvIxg8C6uS43Q0CyorlsQECtNqOzAsC74znrQ4CvKH+tgwCtKGKtAkCnueWKQLU8pG1AgL5kPzvCQLZ+cbZBQKf9sbDAQK/+9iEBwKO0eWyDQKbstukCALB4aymBwLPoMizAgLxxu3kBgKTlLExAsiE/J8EAuydtb4HAsC7lNYCAqPQpd4PAtjYlt4KArjY3asOAvbAzq8HAubxq88HAsyYtd0DAueil4MGAujpyMMJAvntpLoNAq/q8YsCArm6u44PAsmC05YIApGp59MNApyj0tIPAqf8upUNAqzTq4oFAqbulboHArzG0tQJAr+B2PQDAo7Pxr4DAvKCwccOAqeI+NwOAoORn4gEAtX746kKAru0tbIHAvv465ELAvL3gpsEAqmv6IQOAvKVicwJAv6MubIJArKSgTgC4b+T5gUC1eScrgMCvsOvngwCmuDq/gQC2uLb5QgCzbGeogUCmJyBhQIC/f6bxQcCq7rb6QwC4smGGALc98ViAtW+i/YBAuX29/8GArvFmcwEAvnjmaAGAuqZ3uwBAvWn4IINAoy78egIAvWK6Y4MAoS+gIIJAonF+78CAvDv4LwMAovsvrkKAvHTnogNAr75vMEFAvmQtaEBAu6/gtcPAuXSkrgIAuDOp9oGAoDYhKsGApmv7a4EAr3dgMgLAoLFr+YBAs2u4P4OAuiizdUMAqTX8pMDAo3CrOoIAqm7p5oFAorrkPANApen650LAsLLjvADAq2B9tQJAoX01NQIArucrZgGAt2FpsMDAuj6iKIEAr+ehuANAtTRsHYC+f7NrA0CnM39vgsCson54QwCnoDi+A0CmumyvgsCpK7MlQXr1EVJHOKuyF/WSdOm3nDj79lzBA==',
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
            if 'miis' not in email:

                # Only create departments that don't already exist
                try:
                    self.prof_dept = Department.objects.get(name=dept)
                except Department.DoesNotExist:
                    self.stdout.write(bcolors.OKBLUE + '  Creating department ' + dept + bcolors.ENDC)
                    self.prof_dept = Department.objects.create(name=dept)

                # Only create professors that don't already exist
                try:
                    Professor.objects.get(email=email)
                except Professor.DoesNotExist:
                    self.stdout.write(bcolors.OKBLUE + '  Creating professor ' +
                                      first_name + " " + last_name + bcolors.ENDC)
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

        courses_r = requests.get(url + self.term)

        if courses_r.status_code != 200:
            raise CommandError('Unable to retrieve initial course catalog. Status code: %s. URL attempted: %s' % (
                               courses_r.status_code, url + self.term))

        courses_soup = BeautifulSoup(courses_r.text)
        courses_links = courses_soup.find('table').find_all("a")

        for link in courses_links:
            dept = link.string.encode('utf-8')
            self.stdout.write(bcolors.OKBLUE + '  Scraping courses from department ' + dept + bcolors.ENDC)

            course_dept_r = requests.get(department_base_url + link['href'])
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
                            self.professor = Professor.objects.create(first=self.instructor_first,
                                                                      last=self.instructor_last,
                                                                      dept=self.course_dept)

                        try:
                            ProfCourse.objects.get(prof=self.professor, course=self.course)
                        except ProfCourse.DoesNotExist:
                            self.stdout.write(bcolors.OKBLUE + '  Creating ProfCourse ' +
                                              code + ' ' + self.instructor_last + bcolors.ENDC)
                            ProfCourse.objects.create(prof=self.professor, course=self.course)

def get_course_description(crn_url):
    """
    Returns the cleaned course description from the associated CRN page.
    """

    base_url = 'https://ssb.middlebury.edu'

    # Follow the first link to the listing page to get the catalog entry
    listing_r = requests.get(base_url + '/PNTR/' + crn_url)
    listing_soup = BeautifulSoup(listing_r.text)

    # Follow the catalog link to the catalog entry
    try:
        catalog_url = listing_soup.find('a', text='View Catalog Entry')['href']
        catalog_r = requests.get(base_url + catalog_url)
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

