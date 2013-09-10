from django.shortcuts import redirect

def quota_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.get_profile().quota > 0:
            return redirect('quota')
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func