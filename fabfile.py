#from fabric_heroku_postgresql.core import *
from fabric.api import local, env, require

def resetdb():
  local('rm -f rocket/default.db')
  local('python manage.py syncdb --noinput --migrate')
  local('python manage.py loaddata test_data.yaml')
  # local('python manage.py rebuild_index --noinput')

def deploy():
    """fab [environment] deploy"""

    # require('AWS_KEY')
    # require('AWS_SECRET')
    # require('AWS_STORAGE_BUCKET_NAME')
    # require('HEROKU_APP')

    local('heroku maintenance:on')
    local('DJANGO_SETTINGS_MODULE=coursereviews.settings.staging python manage.py collectstatic --noinput')
    local('git push heroku HEAD:master')
    local('heroku run python manage.py syncdb --noinput')
    local('heroku run python manage.py migrate')
    local('heroku run python manage.py collectstatic --noinput')
    local('heroku maintenance:off')
    local('heroku ps')
    local('heroku open')
