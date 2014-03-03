from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.db.models import Count

from reviews.models import Review
from users.models import UserProfile
from .forms import QuotaForm

def index(request):
    return TemplateResponse(request, 'cr_admin/index.html')

def quota(request):
    users_quota_count = UserProfile.objects.values('quota').order_by().annotate(Count('quota'))

    quota_form = QuotaForm()

    return TemplateResponse(request, 'cr_admin/quota.html', {'quota_data': users_quota_count,
                                                             'quota_form': quota_form})

def flags(request):
    return HttpResponse(status=200)