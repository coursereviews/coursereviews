from celery.task import task
from django.contrib.auth.models import User
from users.models import UserProfile
import hashlib, urllib

@task(name='tasks.gravatar_task')
def gravatar_task(new_user, userid):
  gravatar_connection = urllib.urlopen("http://www.gravatar.com/avatar/" + hashlib.md5(new_user.email.lower()).hexdigest())
  gravatar = gravatar_connection.info()['Content-Type']
  if gravatar == "image/png" or (gravatar == "image/jpg" or gravatar == "image/jpeg"):
    profile = User.objects.get(pk=userid).get_profile()
    profile.propic = "http://www.gravatar.com/avatar/" + hashlib.md5(new_user.email.lower()).hexdigest()
    profile.save()