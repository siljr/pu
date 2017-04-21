from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db.models import Q

from questions.forms import QuestionForm, AnswerForm
from questions.models import Question, Answer

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    # makes a dictionary containing all Question objects
    # tabs:newest as default setting
    votes = 0
    for answer in Answer.objects.filter(user = request.user):
        votes += answer.votes

    context = {'questions': Question.objects.filter(user = request.user), 'answers': Answer.objects.filter(user = request.user), 'tabs':'newest', 'myQ':'true', 'votes':votes}

    #search mechanism with Q lookups
    query = request.GET.get("q")
    if query:
        context = {'questions': Question.objects.filter(user=request.user).filter(
            Q(title__contains=query)|
                   Q(body__contains=query)).distinct()}
    # always needs to have a request, a go to html page and a dictrionary
    return render(request, 'profile.html', context)
