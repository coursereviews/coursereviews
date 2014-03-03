from django.conf.urls import patterns, url

urlpatterns = patterns('admin.views',
    url(r'^quota$', 'quota', name='admin_quota'),
    url(r'^flags$', 'flags', name='admin_flags'),
)