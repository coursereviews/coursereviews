from django.conf.urls import patterns, url, include
from registration.views import register

urlpatterns = patterns('users.views',
    url(r'^register/professor/error$', 'professor_registration_error', name='prof_reg_error'),
    url(r'^profile$', 'profile', name="profile"),
)