from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.db.models import Count

from reviews.models import Review
from users.models import UserProfile
from cr_admin.forms import QuotaForm
from cr_admin.models import AdminQuota

def index(request):
    return TemplateResponse(request, 'cr_admin/index.html')

def quota(request):
    users_quota_count = UserProfile.objects.values('quota').order_by().annotate(Count('quota'))

    admin_quota = AdminQuota.objects.get(pk=1)

    quota_form = QuotaForm()

    return TemplateResponse(request, 'cr_admin/quota.html', {'quota_data': users_quota_count,
                                                             'quota_form': quota_form,
                                                             'current_admin_quota': admin_quota})

def flags(request):
    return HttpResponse(status=200)