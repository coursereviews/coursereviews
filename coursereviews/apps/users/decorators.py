from users.models import FirstVisit
from users.models import ViewCount
from django.conf import settings

def first_visit(view_func): 
    """tests to see if its the first time has visited a page

    to use this functionality, set request.user.is_owner to a boolean. Need to check if the user is logged to do that
"""
    def _wrapped_visit_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        
        if request.user.is_authenticated() and hasattr(request.user,'is_owner') and request.user.is_owner and hasattr(response,'template_name'):
            try:
                FirstVisit.objects.get(user=request.user.id, template_path=response.template_name)
            except FirstVisit.DoesNotExist:
                FirstVisit.objects.create(user=request.user, template_path=response.template_name)       
                response.context_data.update({'first_visit': True})
        return response

    return _wrapped_visit_func

def attach_client_ip(view_func):
    def _wrapped_visit_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)

        if not settings.DEBUG:
            ip_address = request.META.get('REMOTE_ADDR', None);
            forwarded_ips_str = request.META.get('x-forwarded-for', None); 
            if forwarded_ips_str:
                forwarded_ips = forwarded_ips_str.split(',');
                ip_address = forwarded_ips[0];
        else:
            ip_address = "76.118.78.216"

        ip_dict = { 'REMOTE_ADDR': ip_address }
        if response.context_data:
            response.context_data.update(ip_dict)
        else:
            response.context_data = ip_dict

        return response
    return _wrapped_visit_func



def view_count(view_func):
    """keeps track of the number of views a page gets
    
    used to keep track of the number of times an anonymous or a non-owner of a page 
    views a certain page of another user. It will not add to the page views if the owner of the page visits the page.
    To use this functionality, you need to set the property of request.user.is_owner to a boolean. 
    The way it has been done is that if request.user is equal to the owner of the page being visited skip_count is set to True
    otherwise it is set to false. Check also if the user is logged in with a request.user.is_authenticated().
    Also the decorator needs to be called at the beginning of the function.
    """
    def _wrapped_visit_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
                
        if not (hasattr(request.user,'is_owner') and request.user.is_owner):
            view_count = ViewCount.objects.get_or_create(url=request.path)[0]
            view_count.increment()

        return response

    return _wrapped_visit_func

