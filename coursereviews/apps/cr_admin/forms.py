from django import forms

class QuotaForm(forms.Form):
    new_quota = forms.IntegerField()
    reset_date = forms.DateField()