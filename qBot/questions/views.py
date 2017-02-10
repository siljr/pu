from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from questions.forms import QuestionForm

from questions.models import Question


def index(request):
    return HttpResponse("Velkommen til qBot!")

def register_question(request):
    form = QuestionForm()
    if request.method =="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            username = form.cleaned_data['user']

            user = User.objects.get(username=username)
            Question.objects.create(title=title, body=body,user=user)
        else:
            form = QuestionForm()

    return render(request, 'question_submission.html',{'form':form,})


