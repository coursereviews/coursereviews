from django import forms

class ProfRegErrorForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    department = forms.CharField(required=True)
    courses = forms.CharField(widget=forms.Textarea, required=False)
