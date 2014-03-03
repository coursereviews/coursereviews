from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# serving up static pages with RequestContext variables
urlpatterns = patterns('reviews.views',
    url(r'^quota$', 'quota', name='quota'),

    url(r'^review/new$', 'create', name='new_review'),
    url(r'^review/(?P<review_id>\d+)$', 'edit', name='edit_review'),
    url(r'^review/(?P<review_id>\d+)/delete$', 'delete', name='delete_review'),

    url(r'^course/(?P<course_slug>[-\w\d]+)$', 'course_detail', name='course_detail'),
    url(r'^professor/(?P<prof_slug>[-\w\d]+)$', 'prof_detail', name='prof_detail'),
    url(r'^course/(?P<course_slug>[-\w\d]+)/(?P<prof_slug>[-\w\d]+)$', 'prof_course_detail', name='prof_course_detail'),    

    url(r'^search$', 'search', name="search"),
)