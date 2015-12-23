from common import *  # noqa

DEBUG = False

STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
