from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages

from cr_admin.models import AdminQuota

def quota_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        profile = request.user.userprofile
        quota = AdminQuota.objects.get(id=1).new_quota
        if profile.professor_assoc or profile.semester_reviews >= quota:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')
    return _wrapped_view_func

def no_professor_access(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.userprofile.professor_assoc:
            return HttpResponse(status=404)
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func
