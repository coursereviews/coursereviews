#from django.conf.urls import patterns, url
from django.conf.urls import *
from users.views import *

urlpatterns = [
    url(r'^register/professor/error$',  # noqa
        professor_registration_error,
        name='prof_reg_error'),
]
