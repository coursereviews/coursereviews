"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up the
following patterns based at whatever URL prefix they are included
under:

* User login at ``login/``.

* User logout at ``logout/``.

* The two-step password change at ``password/change/`` and
  ``password/change/done/``.

* The four-step password reset at ``password/reset/``,
  ``password/reset/confirm/``, ``password/reset/complete/`` and
  ``password/reset/done/``.

The default registration backend already has an ``include()`` for
these URLs, so under the default setup it is not necessary to manually
include these views. Other backends may or may not include them;
consult a specific backend's documentation for details.

"""

from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from django.contrib.auth import views as auth_views
from registration.forms import AuthenticationForm
from static_pages.views import splash
from registration.views import activate
from registration.views import register
from registration.views import professor_register


urlpatterns = patterns('',
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'cr_registration/login.html', 
        'authentication_form': AuthenticationForm},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        { 'next_page': '/' },
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        {'template_name': 'cr_registration/password_change_form.html'},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'cr_registration/password_change_done.html'},
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'template_name': 'cr_registration/password_reset_form.html', 
        'email_template_name': 'cr_registration/password_reset_email.html', 
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

    url(r'^activate/(?P<activation_key>\w+)/$',
        activate,
        { 'template_name': 'cr_registration/activate.html', 'success_url': '/'},
        name='registration_activate'),
    url(r'^register/$',
        register,
        { 'template_name': 'static_pages/splash.html' },
        name='registration_register'),
    url(r'^register/professor/$', professor_register, name='professor_register'),
    url(r'^register/sent$', 
        splash, 
        { 'message': 'Thanks for signing up!', 'sub_message': 'We sent your email an account activation link.'}, 
        name='registration_complete'),
    url(r'^register/closed/$',
       TemplateView.as_view(template_name='cr_registration/registration_closed.html'),
       name='registration_disallowed'),
)