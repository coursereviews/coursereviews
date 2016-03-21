"""Development settings and globals."""

from os.path import join, normpath
from boto.s3.connection import OrdinaryCallingFormat
from common import *  # noqa

# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(DJANGO_ROOT, 'default.db')),
        'USER': '',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Setting CELERY_ALWAYS_EAGER = True makes the tasks blocking, just run celeryd instead
CELERY_ALWAYS_EAGER = True

ALLOWED_HOSTS = ['*']

STATICFILES_STORAGE = 'coursereviews.settings.storage.S3PipelineStorage'
# STATICFILES_STORAGE = 'coursereviews.settings.storage.NonPackagingS3PipelineStorage'

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
# BROKER_TRANSPORT = 'amqplib'

# Set this number to the amount of allowed concurrent connections on your AMQP
# provider, divided by the amount of active workers you have.
#
# For example, if you have the 'Little Lemur' CloudAMQP plan (their free tier),
# they allow 3 concurrent connections. So if you run a single worker, you'd
# want this number to be 3. If you had 3 workers running, you'd lower this
# number to 1, since 3 workers each maintaining one open connection = 3
# connections total.
#
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-pool-limit
BROKER_POOL_LIMIT = 3

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-connection-max-retries
BROKER_CONNECTION_MAX_RETRIES = 0

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-url
# BROKER_URL = environ.get('RABBITMQ_URL') or environ.get('CLOUDAMQP_URL')

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'amqp'

AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
