from django.conf.urls import patterns, url

urlpatterns = patterns('users.views',
    url(r'^register/professor/error$',  # noqa
        'professor_registration_error',
        name='prof_reg_error'),
)
