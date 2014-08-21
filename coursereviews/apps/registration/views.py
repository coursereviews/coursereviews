from django.shortcuts import redirect
from django.contrib import messages
from users.models import UserProfile
from reviews.models import Professor
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from registration import signals
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile
from django.template.response import TemplateResponse

def activate(request, activation_key, template_name='registration/activate.html'):
    user = RegistrationProfile.objects.activate_user(activation_key)
    if user:
        signals.user_activated.send(sender=RegistrationProfile, user=user, request=request)
        messages.add_message(request, messages.INFO, "Your account was successfully activated!")
        return redirect('auth_login')
    else:
        return TemplateResponse(request, template_name, {'activation_key': activation_key})


def register(request, template_name='static_pages/splash.html'):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data['email'].split('@')[0]
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            if Site._meta.installed:
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)
            new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, site)
            signals.user_registered.send(sender=RegistrationProfile,
                                         user=new_user,
                                         request=request)
            profile = UserProfile.objects.get(user=new_user)
            profile.save()

            # Check if the email matches a professor in the db
            try:
                professor = Professor.objects.get(email=email)
                profile.professor_assoc = professor
                profile.save()
            except Professor.DoesNotExist:
                # Not a professor in our db, but user came from
                # professor registration page
                if request.POST.get('is_professor', False):
                    # is_professor field is only for validation
                    return redirect('prof_reg_error')
                # else drop down to normal registration

            messages.add_message(request, messages.INFO, "Thanks for signing up! Check your email for an activation link.")
            success_url = request.GET.get('next')
            if success_url:
                return redirect(success_url)
            else:
                return redirect('index')
    else:
        form = RegistrationForm()
    return TemplateResponse(request, template_name, {'form': form})


def professor_register(request, template_name='cr_registration/professor_registration_form.html'):
    # if request.user.is_authenticated():
        # return redirect('index')
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            try:
                professor = Professor.objects.get(email=form.cleaned_data['email'])
                return register(request, template_name='cr_registration/professor_registration_form.html')
            except Professor.DoesNotExist:
                return redirect('prof_reg_error')

        else:
            return TemplateResponse(request, template_name, {'form': form})

    else:
        form = RegistrationForm()
    return TemplateResponse(request, template_name, {'form': form})

@login_required
def password_change_done(request):
    messages.add_message(request, messages.INFO, "Password successfully changed!")
    return redirect('index')