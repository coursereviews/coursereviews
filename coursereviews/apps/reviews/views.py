from django.template.response import TemplateResponse

def browse(request):
    return TemplateResponse(request, 'reviews/browse.html')