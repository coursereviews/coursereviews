from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

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
