from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

# import django_filepicker

# User Profile
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=100, blank=True)
	# propic = models.CharField(max_length=200, blank=True)
 
 	# def get_absolute_url(self):
		# return reverse('users.views.profile', args=[self.user])

	def get_display_name(self):
		if self.name:
			return self.name
		return self.user.username

	def __unicode__(self):
		return self.user.username

# Handles user profile creation if not already created
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
    	profile = UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class FirstVisit(models.Model):
	template_path = models.CharField(max_length=100, blank=True)
	user = models.ForeignKey('auth.User')


class ViewCount(models.Model):
	url = models.URLField()
	count = models.IntegerField(default=0)

	def increment(self):
		self.count += 1
		self.save()
