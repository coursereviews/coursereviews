from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from static_pages.views import http403, http404, http500

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'static_pages.views.home', name='home'),
    url(r'^about/$', 'static_pages.views.about', name='about'),    
    url(r'^contact/$', 'static_pages.views.contact', name='contact'),
    url(r'', include('registration.auth_urls')),
    url(r'', include('registration.backends.default.urls')),
    # url(r'^reviews/', include('reviews.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # api patterns      
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()

urlpatterns = format_suffix_patterns(urlpatterns)

handler403 = http403
handler404 = http404
handler500 = http500