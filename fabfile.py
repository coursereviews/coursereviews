from datetime import date

from fabric.api import local, env, require, warn_only
from fabric.utils import puts
from fabric.colors import blue

def resetdb():
    local('rm -f coursereviews/default.db')
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

def capture_db():
    # We follow the flow outlined here:
    # https://devcenter.heroku.com/articles/heroku-postgres-import-export#export
    db_name = 'middcourses-{:%Y-%m-%d}'.format(date.today())

    # We do not want to abort on unreconized parameter "lock_timeout"
    with warn_only():
        local('heroku pgbackups:capture')
        local('curl -o {0}.dump `heroku pgbackups:url`'.format(db_name))
        local('createdb {0}'.format(db_name))
        local('pg_restore --no-acl --no-owner -h localhost -U {0} -d {1} "{1}.dump"'.format(env.user, db_name))

        puts(blue('PostgreSQL database {0} created'.format(db_name)))