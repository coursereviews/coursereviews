"""Settings and globals for both development and production."""

from datetime import timedelta
from sys import path
from os.path import abspath, basename, dirname, join, normpath
from djcelery import setup_loader
from os import environ


# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
path.append(join(DJANGO_ROOT, 'apps'))

# safety precaution. Exception to the rule where we DRY with inherited settings files.
DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS = (
    ('Teddy Knox', 'teddy@rocketlistings.com'),
    ('Dana Silver', 'dsilver1221@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'America/New_York'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# AWS_S3_CUSTOM_DOMAIN = 'static.rocketlistings.com'
# S3_URL = 'http://static.rocketlistings.com/'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(DJANGO_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(DJANGO_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = environ.get('SECRET_KEY', 'imnotwearingpants')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(DJANGO_ROOT, 'fixtures')),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    # "listings.context_processors.s3_url",
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(DJANGO_ROOT, 'templates')),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Use GZip compression to reduce bandwidth.
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME

DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    # Database migration helpers:
    'south',

    # Asynchronous task queue:
    'djcelery',

    # search
    'haystack',

    # pagination template tags
    'pagination',

    # static file management 
    'pipeline',

    # rest support
    'rest_framework',

    # select multiple fields
    'multiselectfield'

)

LOCAL_APPS = (
    'reviews',
    'registration',
    'static_pages',
    'users',
    'cr_admin',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    'require_debug_false': {
        '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# APPEND_SLASH = False
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.ModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'

############# PIPELINE CONFIG
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_CSSMIN_BINARY = 'cssmin'
# PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'
PIPELINE_JS_COMPRESSOR = None
PIPELINE_DISABLE_WRAPPER = True
PIPELINE_COMPILERS = (
  'pipeline.compilers.less.LessCompiler',
)

PIPELINE_CSS = {
    'local_bs': {
        'source_filenames': (
            'coursereviews/vendorcss/bootstrap-glyphicons.css',
            'coursereviews/vendorcss/bootstrap.min.css',
        ),
        'output_filename': 'css/bootstrap.css',
        'variant': 'datauri',
    },
    'base': {
        'source_filenames': (
            'coursereviews/less/base.less',
        ),
        'output_filename': 'css/base.css',
        'variant': 'datauri',
    },
    'reviews': {
        'source_filenames': (
            'coursereviews/vendorcss/select2.css',
            'coursereviews/vendorcss/slider.css',
            'reviews/less/reviews.less',
        ),
        'output_filename': 'css/listings.css',
        'variant': 'datauri',
    },
    'static_pages': {
        'source_filenames': (
            'static_pages/less/static_pages.less',
        ),
        'output_filename': 'css/static_pages_base.css',
        'variant': 'datauri',
    },
    'users': {
        'source_filenames': (
            'users/less/users.less',
        ),
        'output_filename': 'css/user.css',
        'variant': 'datauri',
    },
}

PIPELINE_JS = {
    'local_libs_development' : {
        'source_filenames': (
            'coursereviews/js/jquery-1.9.0.js',
            'coursereviews/js/bootstrap/bootstrap.min.js',
            'coursereviews/js/global.js',
        ),
        'output_filename': 'js/libs.js'
    },
    'local_libs_production' : {
        'source_filenames': (
            'coursereviews/js/global.js',
        ),
        'output_filename': 'js/libs.js'
    },
}

############# AWS CONFIG
S3_URL = 'http://static.middcourses.com/'
AWS_ACCESS_KEY_ID = environ.get('AWS_KEY', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET', '')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = 'static.middcourses.com'
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False
AWS_HEADERS = {
        'Cache-Control': 'max-age=300, s-maxage=900, public, no-transform'
}
# backend storages.backends.s3boto.S3BotoStorage
# STATIC_URL = S3_URL + 'assets/'


############# CELERY CONFIG
# See: http://celery.readthedocs.org/en/latest/configuration.html#celery-task-result-expires
CELERY_TASK_RESULT_EXPIRES = timedelta(minutes=30)

# See: http://celery.github.com/celery/django/
setup_loader()

CELERY_IMPORTS = ('registration.tasks')

############# USER ACCOUNTS CONFIG
AUTH_PROFILE_MODULE = 'users.UserProfile'

ACCOUNT_ACTIVATION_DAYS = 7

DEFAULT_FROM_EMAIL = 'dana@middcourses.com'

LOGIN_URL = '/login/' # references users/urls.py name

LOGOUT_URL = '/logout/' #references users/urls.py name

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/login'

# HAYSTACK CONFIG
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': join(dirname(__file__), 'whoosh_index'),
    }
}