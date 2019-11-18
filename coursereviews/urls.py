#from django.conf.urls import patterns, include, url
from django.conf.urls import *
from django.contrib import admin
from django.contrib import admindocs
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from static_pages.views import about, contact, index, google_verify, http403, http404, http500

admin.autodiscover()

urlpatterns = [
    url(r'^$', index, name='index'),  # noqa
    url(r'^about/$', about, name='about'),
    url(r'^contact/$', contact, name='contact'),
    url(r'', include('registration.urls')),
    url(r'', include('reviews.urls')),
    url(r'', include('users.urls')),
    url(r'^admin/', include('cr_admin.urls')),
    url(r'^stats/', include('stats.urls')),
    # url(r'^users/', include('users.urls')),

    url(r'^google(?P<code>[0-9a-f]{16})\.html$', google_verify),

    url(r'^djadmin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^djadmin/', admin.site.urls),

    # api patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)

handler403 = http403
handler404 = http404
handler500 = http500
