from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from reviews.models import Review, Professor, Course
from reviews.forms import ReviewForm

def browse(request):
    profs = Professor.objects.all()[:5]
    courses = Course.objects.all()[:5]
    return TemplateResponse(request, 'reviews/browse.html', { 'profs': profs, 'courses': courses })

@require_GET
def create(request):
  form = ReviewForm()
  return TemplateResponse(request, 'reviews/edit.html', {'form': form})

def detail(request, review_id, edit=False):
  review = Review.objects.select_related().get(id=review_id)
  if edit == True:
    form = ReviewForm(instance=review)
    return TemplateResponse(request, 'reviews/edit.html', {'form': form})
  else:
    return TemplateResponse(request, 'reviews/view.html', {'review': review})
