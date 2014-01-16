from django import forms
from reviews.models import Review

class ReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    exclude = ('user')
    widgets = {
        'components': forms.SelectMultiple(),
        'again': forms.RadioSelect(),
        'another': forms.RadioSelect(),
        'grasp': forms.RadioSelect(),
        'value': forms.SelectMultiple(),
        'why_take': forms.SelectMultiple()
    }
