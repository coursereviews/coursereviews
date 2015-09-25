from django.http import Http404

def middcourses_admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.userprofile.middcourses_admin:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404
    return _wrapped_view_func

def middcourses_moderator_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.userprofile.middcourses_moderator:
            return view_func(request, *args, **kwargs)
        else:
            raise Http404
    return _wrapped_view_func