from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_page
from django.template.response import TemplateResponse
from django.http import HttpResponse
from users.decorators import attach_client_ip
from reviews.views import browse
import os

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def http403(request):
    return render(request, 'static_pages/403.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def http404(request):
    return render(request, 'static_pages/404.html')

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(60 * 15)
def http500(request):
    return render(request, 'static_pages/500.html')

def index(request):
    if request.user.is_authenticated():
        return browse(request)
    else:
        return splash(request)

# @cache_page(60 * 15)
# @cache_control(must_revalidate=True, max_age=3600)
def splash(request, **kwargs):
    return TemplateResponse(request, 'static_pages/splash.html', kwargs)

# @cache_control(must_revalidate=True, max_age=3600)
# @cache_page(60 * 15)
def contact(request):
    return TemplateResponse(request, 'static_pages/contact.html')

# @cache_control(must_revalidate=True, max_age=3600)
# @cache_page(60 * 15)
def about(request):
    return TemplateResponse(request, 'static_pages/about.html')

def google_verify(request, code):
    google_verification_code = os.environ.get('GOOGLE_VERIFICATION_CODE')

    if code == google_verification_code:
        print google_verification_code
        return TemplateResponse(request,
            'static_pages/google_verify.html',
            {'google_verification_code': google_verification_code})
    else:
        return HttpResponse(404)
