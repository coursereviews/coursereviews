from django import forms
from django.forms import ModelChoiceField
from reviews.models import Review, ProfCourse

class ReviewForm(forms.ModelForm):
    prof_course = ModelChoiceField(ProfCourse.objects.all(), empty_label=None)

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
