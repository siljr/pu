from django import forms

class QuestionForm(forms.Form):
    title = forms.CharField(max_length=128)
    body = forms.CharField()
    tags = forms.CharField()

class AnswerForm(forms.Form):
    body = forms.CharField(label='body')
