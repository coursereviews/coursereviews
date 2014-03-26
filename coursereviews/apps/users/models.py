from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from reviews.models import Professor

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=100, blank=True)
	quota = models.IntegerField(max_length=2, default=2)
	total_reviews = models.IntegerField(default=0)
	professor_assoc = models.ForeignKey(Professor, related_name='user_profile', null=True)
	middcourses_admin = models.BooleanField(default=False)
	middcourses_moderator = models.BooleanField(default=False)

	def get_display_name(self):
		if self.name:
			return self.name
		return self.user.username

	def __unicode__(self):
		return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

class FirstVisit(models.Model):
	template_path = models.CharField(max_length=100, blank=True)
	user = models.ForeignKey('auth.User')

class ViewCount(models.Model):
	url = models.URLField()
	count = models.IntegerField(default=0)

	def increment(self):
		self.count = F('count') + 1
		self.save()