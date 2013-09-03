from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_page
from django.template.response import TemplateResponse
from users.decorators import attach_client_ip
from reviews.views import browse

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

def index(request, **kwargs):
    if request.user.is_authenticated():
        return browse(request, **kwargs)
    else:
        return splash(request, **kwargs)

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