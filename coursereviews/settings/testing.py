from common import *  # noqa

DEBUG = False

STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'

DATABASES['default']['ENGINE'] = 'django_postgrespool'
