from django.core.management.base import BaseCommand

from reviews.models import Department

class Command(BaseCommand):
    args = ''
    help = "Removes all courses and professors the database."

    def handle(self, *args, **options):
        Department.objects.all().delete()
