from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from catalog.scraper import Scraper
from catalog.models import Term

class Command(BaseCommand):
    help = 'Adds courses from the specified term to the database.'

    option_list = BaseCommand.option_list + (
        make_option('--term', help='Specify the term. Ex: 201590'),
    )

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

    def handle(self, *args, **kwargs):
        term = self.validate_term(kwargs['term'])
        catalog = self.create_catalog(term.id)

        print(catalog)
