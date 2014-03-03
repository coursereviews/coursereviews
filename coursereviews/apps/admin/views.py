from django.http import HttpResponse
from django.template.response import TemplateResponse

from reviews.models import Review

def index(request):
    
    return TemplateResponse(request, 'cr_admin/index.html')

def quota(request):
    return HttpResponse(status=200)

def flags(request):
    return HttpResponse(status=200)