from django.conf.urls import patterns, url

urlpatterns = patterns('cr_admin.views',
    url(r'^$', 'index', name='admin_index'),
    url(r'^quota$', 'quota', name='admin_quota'),
    url(r'^flags$', 'flags', name='admin_flags'),
    url(r'^review/(?P<review_id>\d+)$', 'flagged_review', name='admin_review'),
)