from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseForbidden

from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.core.mail import send_mail
from django.conf import settings

from users.forms import ProfRegErrorForm 

def professor_registration_error(request):
    if request.user.is_authenticated():
        return redirect('index')

    if request.method == 'POST':
        form = ProfRegErrorForm(request.POST)
        if form.is_valid():
            ctx = {'name': form.cleaned_data['name'],
                   'email': form.cleaned_data['email'],
                   'department': form.cleaned_data['department'],
                   'courses': form.cleaned_data['courses'] }
            message = render_to_string('users/prof_reg_error_mail.txt', ctx)
            send_mail('MiddCourses Prof Registration', message, settings.DEFAULT_FROM_EMAIL, ['dsilver@middlebury.edu'])
            return TemplateResponse(request, 'users/prof_reg_error_submitted.html', {'name': form.cleaned_data['name']})
        else:
            return TemplateResponse(request, 'users/prof_reg_error.html', {'form': form})

    else:
        form = ProfRegErrorForm()
        return TemplateResponse(request, 'users/prof_reg_error.html', {'form': form})