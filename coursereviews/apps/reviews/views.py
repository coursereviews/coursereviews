from django.template.response import TemplateResponse

def browse(request, **kwargs):
    return TemplateResponse(request, 'reviews/browse.html', **kwargs)