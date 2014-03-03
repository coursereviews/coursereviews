from django.http import HttpResponse

from reviews.models import Review

def quota(request):
    return HttpResponse(status=200)

def flags(request):
    return HttpResponse(status=200)