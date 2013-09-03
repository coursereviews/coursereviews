from django.template.response import TemplateResponse
from reviews.models import Professor, Course

def browse(request):
    profs = Professor.objects.all()[:5]
    courses = Course.objects.all()[:5]
    return TemplateResponse(request, 'reviews/browse.html', { 'profs': profs, 'courses': courses })