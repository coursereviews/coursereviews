from datetime import datetime

from fabric.api import local, env
from fabric.contrib.console import confirm
from fabric.utils import puts, indent
from fabric.colors import blue, green

def reset_db():
    local('psql -c "drop database if exists middcourses"')
    local('psql -c "create database middcourses"')
    local('python manage.py migrate')

def deploy():
    """fab [environment] deploy"""

    # require('AWS_KEY')
    # require('AWS_SECRET')
    # require('AWS_STORAGE_BUCKET_NAME')
    # require('HEROKU_APP')

    local('heroku maintenance:on')
    local('DJANGO_SETTINGS_MODULE=coursereviews.settings.staging python manage.py collectstatic --noinput')  # noqa
    local('git push heroku HEAD:master')
    local('heroku run python manage.py migrate')
    local('heroku run python manage.py collectstatic --noinput')
    local('heroku maintenance:off')
    local('heroku ps')

def list_databases(middcourses_only='true'):
    """
    List all the databases in the currently running PostgreSQL installation.

    By default only list databases beginning with "middcourses".
    """

    if middcourses_only == 'true':
        query = 'psql -t -c "select datname from pg_database where datname like \'middcourses%\'"'
    else:
        query = 'psql -t -c "select datname from pg_database"'

    databases = local(query, capture=True)
    databases = [db.strip(' ') for db in databases.split('\n')]

    puts(blue('Databases:'))
    for db in databases:
        puts(indent(db, spaces=2))


def capture_db():
    """
    Create a backup of the production database using Heroku PG Backups.
    Download the backup to a PostgreSQL dump file.
    Restore the backup to the locally running PostgreSQL instance.
    Optionally remove the dump file.
    """

    # We follow the flow outlined here:
    # https://devcenter.heroku.com/articles/heroku-postgres-import-export#export
    now = datetime.now().replace(microsecond=0)
    db_name = 'middcourses-{0}'.format(now.isoformat())

    puts(blue('Creating a backup.'))
    local('heroku pg:backups capture')

    puts(blue('Downloading the backup.'))
    local('curl -o {0}.dump `heroku pg:backups public-url`'.format(db_name))

    puts(blue('Restoring the database to PostgreSQL.'))
    local('createdb {0}'.format(db_name))
    local('pg_restore --no-acl --no-owner -h localhost -U {0} -d {1} "{1}.dump"'.format(env.user, db_name))  # noqa

    puts(green('PostgreSQL database {0} created.'.format(db_name)))

    remove = confirm('Remove "{0}.dump"?'.format(db_name))

    if remove:
        local('rm {0}.dump'.format(db_name))
