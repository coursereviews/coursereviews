from django.shortcuts import redirect
from django.http import HttpResponse

def quota_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.get_profile().quota > 0:
            return redirect('quota')
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def no_professor_access(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.get_profile().professor_assoc != None:
            return HttpResponse(status=404)
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func
