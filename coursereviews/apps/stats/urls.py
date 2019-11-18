#from django.conf.urls import patterns, url
from django.conf.urls import *
from stats.views import stats

urlpatterns = [
    url(r'^$', stats, name='stats.stats'),  # noqa
]
