from __future__ import print_function, unicode_literals

from django.core.management.base import BaseCommand
from django.utils.termcolors import colorize
from lxml import html
from lxml.cssselect import CSSSelector
import requests
from reviews.models import Professor


class Command(BaseCommand):
    help = """Adds the Middlebury webid to each professor in the database.

           Some professors already in the database may not be in the current
           Middlebury directory. This is common for visiting Winter term professors.
           """

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='Don\'t save webids.')

    @staticmethod
    def get_professors_directory_post_data():
        """Get the POST data required to search for all the faculty in the
        Middlebury directory.
        """

        res = requests.get('https://directory.middlebury.edu/default.aspx')
        tree = html.fromstring(res.text)
        inputs = CSSSelector('#aspnetForm input')(tree)

        fields = [(i.get('name'), i.get('value')) for i in inputs]
        fields.append(
            ('ctl00$ctl00$PageContent$PageContent$middDirectoryForm$ddlType',
             'Faculty'),
        )

        return dict(fields)

    @classmethod
    def get_professors_webid_email(cls):
        """Get a list of dictionaries of professors' webid and email from
        the Middlebury directory.
        """

        data = cls.get_professors_directory_post_data()
        res = requests.post('https://directory.middlebury.edu/default.aspx', data=data)
        tree = html.fromstring(res.text)

        professors = CSSSelector('.ResultItem')(tree)
        td_a = CSSSelector('td a')

        return [{'webid': td_a(prof)[0].get('href')[1:], 'email': td_a(prof)[1].text}
                for prof in professors]

    def handle(self, *args, **kwargs):
        """Add the midd_webid field to all professors found in the current
        Middlebury directory.
        """

        if kwargs['dry_run']:
            print(colorize('Dry run. Nothing will be saved.', fg='yellow'))

        professors = self.get_professors_webid_email()
        added = 0

        for directory_prof in professors:
            try:
                middcourses_prof = Professor.objects.get(email=directory_prof['email'])
                middcourses_prof.midd_webid = directory_prof['webid']

                if not kwargs['dry_run']:
                    middcourses_prof.save()
                added += 1
            except Professor.DoesNotExist:
                pass

        print(colorize('Added webids for {} professors.'.format(added), fg='green'))
