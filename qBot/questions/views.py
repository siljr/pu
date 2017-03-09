from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.views import generic
from django.db.models import Q

from questions.forms import QuestionForm
from .models import Question

@login_required(login_url='/login/')
def index(request):
    # makes a dictionary containing all Question objects
    # tabs:newest as default setting
    context = {'questions': reversed(Question.objects.all()), 'tabs':'newest'}

    #search mechanism with Q lookups
    query = request.GET.get("q")
    if query:
        context = {'questions': Question.objects.filter(
            Q(title__contains=query)|
                   Q(body__contains=query)).distinct()}
    # always needs to have a request, a go to html page and a dictrionary
    return render(request, 'index.html', context)

#Views for spørsmål sortert etter nyest og eldst
def newest(request):
    # makes a dictionary containing all Question objects
    context = {'questions': reversed(Question.objects.all().order_by("created_at")), 'tabs':'newest'}
    return render(request, 'index.html', context)

def oldest(request):
    context = {'questions': Question.objects.all().order_by("created_at"), 'tabs':'oldest'}
    return render(request, 'index.html', context)

def most_votes(request):
    # for now:
    context = {'questions': Question.objects.all(), 'tabs': 'most_votes'}
    """for later:
    context = {'questions': Question.objects.all().order_by("votes"), 'tabs': 'most_votes'} """
    return render(request, 'index.html', context)

@login_required(login_url='/login/')
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

                # when you submit one question, you are redirected back to the main page
                return redirect('/questions')

            else:
                form = QuestionForm()

    return render(request, 'question_submission.html',{'form': form, })

# @login_required(login_url='/login')
# def upvote_question(request):
#     username = None
#     if request.method == "POST":
#         username = request.user.username
#         question = request.question.id
#
#         # pseudokode
#
#




#    return redirect('/questions')



@login_required(login_url='/login/')
def myquestions(request):
    # makes a dictionary containing all Question objects
    # tabs:newest as default setting
    context = {'questions': Question.objects.filter(user = request.user), 'tabs':'newest'}

    #search mechanism with Q lookups
    query = request.GET.get("q")
    if query:
        context = {'questions': Question.objects.filter(
            Q(title__contains=query)|
                   Q(body__contains=query)).distinct()}
    # always needs to have a request, a go to html page and a dictrionary
    return render(request, 'index.html', context)

#Views for spørsmål sortert etter nyest og eldst
def myQnewest(request):
    # makes a dictionary containing all Question objects
    context = {'questions': Question.objects.filter(user=request.user), 'tabs': 'newest'}
    return render(request, 'index.html', context)

def myQoldest(request):
    context = {'questions': Question.objects.filter(user=request.user).order_by("created_at"), 'tabs':'oldest', 'myQ':'true'}
    return render(request, 'index.html', context)

def myQmost_votes(request):
    # for now:
    context = {'questions': Question.objects.filter(user=request.user), 'tabs': 'most_votes', 'myQ':'true'}
    """for later:
    context = {'questions': Question.objects.all().order_by("votes"), 'tabs': 'most_votes'} """
    return render(request, 'index.html', context)
