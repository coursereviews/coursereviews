from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# serving up static pages with RequestContext variables
urlpatterns = patterns('reviews.views',
    url(r'^/new_review$', 
      TemplateView.as_view(template_name='reviews/new_review.html'), name='new_review'),
)