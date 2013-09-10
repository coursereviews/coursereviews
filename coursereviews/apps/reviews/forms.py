from django import forms
from reviews.models import Review

class ReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    exclude = ('user')
    widgets = {
        'value': forms.RadioSelect(),
        'find': forms.RadioSelect(),
        'atmosphere': forms.RadioSelect(),
        'deserving': forms.RadioSelect(),
        'help': forms.RadioSelect(),
        'another': forms.RadioSelect(),
        'recommend': forms.RadioSelect(),
    }
