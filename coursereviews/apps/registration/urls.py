#from django.conf.urls import patterns, url
from django.conf.urls import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, \
        PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
        PasswordResetDoneView
from registration.forms import AuthenticationForm
from registration.views import (activate,
                                register,
                                professor_register,
                                password_change_done)

# Activation keys get matched by \w+ instead of the more specific
# [a-fA-F0-9]{40} because a bad activation key should still get to the view;
# that way it can return a sensible "invalid key" message instead of a
# confusing 404.

urlpatterns = [
    url(r'^login/$', LoginView.as_view(),  # noqa
        {'template_name': 'cr_registration/login.html',
        'authentication_form': AuthenticationForm},
        name='login'),

    url(r'^logout/$',
        LogoutView.as_view(),
        {'next_page': '/'},
        name='logout'),

    url(r'^password/change/$',
        PasswordChangeView.as_view(),
        {'template_name': 'cr_registration/password_change_form.html',
         'post_change_redirect': '/password/change/done'},
        name='password_change'),

    url(r'^password/change/done/$',
        password_change_done,
        name='password_change_done'),

    url(r'^password/reset/$',
        PasswordResetView.as_view(),
        {'template_name': 'cr_registration/password_reset_form.html',
        'email_template_name': 'cr_registration/password_reset_email.txt',
        'subject_template_name': 'cr_registration/password_reset_subject.txt'},
        name='password_reset'),

    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        PasswordResetConfirmView,
        {'template_name': 'cr_registration/password_reset_confirm.html'},
        name='password_reset_confirm'),

    url(r'^password/reset/complete/$',
        PasswordResetCompleteView,
        {'template_name': 'cr_registration/password_reset_complete.html'},
        name='password_reset_complete'),

    url(r'^password/reset/done/$',
        PasswordResetDoneView,
        {'template_name': 'cr_registration/password_reset_done.html'},
        name='password_reset_done'),

    url(r'^activate/(?P<activation_key>\w+)/$', activate,
        {'template_name': 'cr_registration/activate.html'},
        name='registration_activate'),

    url(r'^register/$', register, name='registration_register'),

    url(r'^register/professor/$', professor_register, name='professor_register'),
]
