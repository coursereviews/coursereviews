#from django.conf.urls import patterns, url
from django.conf.urls import *
from cr_admin.views import *

urlpatterns = [
    url(r'^$', index, name='admin_index'),  # noqa
    url(r'^quota$', quota, name='admin_quota'),
    url(r'^flags$', flags, name='admin_flags'),
    url(r'^flags/moderated$', flags_moderated, name='admin_flags_moderated'),
    url(r'^review/(?P<review_id>\d+)$', flagged_review, name='admin_review'),
]
