from django.conf.urls import *
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from registration.forms import AuthenticationForm
from static_pages.views import splash
from registration.views import (activate,
                                register,
                                professor_register,
                                password_change_done)

urlpatterns = patterns('',
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.

    # this is how we interface with the django authentication
    url(r'^login/$', auth_views.login,
        {'template_name': 'cr_registration/login.html',
        'authentication_form': AuthenticationForm },
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        { 'next_page': '/' },
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        {'template_name': 'cr_registration/password_change_form.html',
         'post_change_redirect': '/password/change/done'},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'template_name': 'cr_registration/password_reset_form.html',
        'email_template_name': 'cr_registration/password_reset_email.txt',
        'subject_template_name': 'cr_registration/password_reset_subject.txt'},
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'cr_registration/password_reset_confirm.html'},
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'cr_registration/password_reset_complete.html'},
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'cr_registration/password_reset_done.html'},
        name='auth_password_reset_done'),

    url(r'^activate/(?P<activation_key>\w+)/$', activate,
        {'template_name': 'cr_registration/activate.html'},
        name='registration_activate'),
    url(r'^register/$', register, name='registration_register'),
    url(r'^register/professor/$', professor_register, name='professor_register'),
)