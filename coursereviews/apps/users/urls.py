from django.conf.urls import patterns, url, include
from registration.views import register
from django.views.generic import TemplateView


from registration.backends.default.urls import *
from registration.auth_urls import *