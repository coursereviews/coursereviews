from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from users.models import UserProfile
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from registration.backend import Backend
from django import forms
from registration.forms import RegistrationForm
from django.forms.util import ErrorList

def activate(request, backend,
             template_name='registration/activate.html',
             success_url=None, extra_context=None, **kwargs):
    backend = Backend()
    account = backend.activate(request, **kwargs)

    if account:
        if success_url is None:
            to, args, kwargs = backend.post_activation_redirect(request, account)
            return redirect(to, *args, **kwargs)
        else:
            return redirect(success_url)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)


def register(request, success_url=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None):
    backend = Backend()
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.cleaned_data['username'] = form.cleaned_data['email'].split('@')[0]
            new_user = backend.register(request, **form.cleaned_data)
            profile = UserProfile.objects.get(user=new_user)
            profile.save()
            if request.GET.get('next',''):
                success_url = request.GET.get('next','')
                return redirect(success_url)
            elif success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        form = RegistrationForm()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name, {'form': form}, context_instance=context)