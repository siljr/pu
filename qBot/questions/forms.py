from django import forms

class QuestionForm(forms.Form):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=1000000)
    user = forms.CharField(max_length=1024)
