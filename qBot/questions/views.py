from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from questions.forms import QuestionForm

from questions.models import Question


def index(request):
    return HttpResponse("Velkommen til qBot!")

def register_question(request):
    form = QuestionForm()
    if request.method == "POST":
        username = None
        form = QuestionForm(request.POST)
        if request.user.is_authenticated():
            username = request.user.username
            if form.is_valid():
                title = form.cleaned_data['title']
                body = form.cleaned_data['body']

                user = User.objects.get(username=username)

                Question.objects.create(title=title, body=body, user=user)

            else:
                form = QuestionForm()

    return render(request, 'question_submission.html',{'form': form, })
