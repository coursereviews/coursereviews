from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages

from cr_admin.models import AdminQuota

def quota_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        profile = request.user.get_profile()
        quota = AdminQuota.objects.get(id=1).new_quota
        if not profile.professor_assoc and profile.semester_reviews > quota:
            messages.add_message(request, messages.INFO, "You have to write some reviews before you can see that.")
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def no_professor_access(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.get_profile().professor_assoc:
            return HttpResponse(status=404)
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func
