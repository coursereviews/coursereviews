from django import forms
from reviews.models import Review

class ReviewForm(forms.ModelForm):

  class Meta:
    model = Review
    exclude = ('user', 'flagged', 'flagged_by', 'flagged_count',
               'up_votes', 'down_votes')
    widgets = {
        'components': forms.SelectMultiple(),
        'again': forms.RadioSelect(),
        'another': forms.RadioSelect(),
        'grasp': forms.RadioSelect(),
        'value': forms.SelectMultiple(),
        'why_take': forms.SelectMultiple()
    }
