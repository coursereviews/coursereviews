from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# serving up static pages with RequestContext variables
urlpatterns = patterns('reviews.views',
    url(r'^new$', 'create', name='new_review'),
    url(r'^(?P<review_id>\d+)$', 'detail', {'edit': False}, name='view_review'),
    url(r'^(?P<review_id>\d+)/edit$', 'detail', {'edit': True}, name='edit_review'),
    url(r'^(?P<review_id>\d+)/delete$', 'delete', name='delete_review'),
)