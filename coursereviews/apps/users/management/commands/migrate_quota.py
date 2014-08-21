from django.core.management.base import NoArgsCommand

from django.contrib.auth.models import User

class Command(NoArgsCommand):
    help = "Migrate users to review counting quota system."

    def handle_noargs(self, **options):
        users = User.objects.all().select_related('review')

        for user in users:
            profile = user.get_profile()

            profile.total_reviews = user.reviews.all().count()
            profile.save()