from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from questions.forms import QuestionForm
from .models import Question

@login_required(login_url='/login/')
def index(request):
    # makes a dictionary containing all Question objects
    context = {'questions': Question.objects.all()}
    # always needs to have a request, a go to html page and a dictrionary
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

    return render(request, 'question_submission.html',{'form': form,})




@login_required(login_url='/login/')
def vote(request):

    user = request.user
    if request.method == "GET":

        question_id = request.GET.get('question', '')
        question = Question.objects.get(id=question_id)
        if request.GET.get('votetype', '') == 'up':
            print('**********')
            print(question.user_votes)
            print('**********')
            if question.is_in_user_votes(user):
                question.downvote_question(user)
                print("Downvoted")

            else:
                question.upvote_question(user)
                print('upvoted')
                return render(request, "index.html", {'questions': Question.objects.all(), "href" :"/questions/vote?question={{ "+str(question.id)+" }}&votetype=up", 'this.queston.active_button': "True", 'id':question_id})
        else:
            print('ingen av delene')
    else:
        print('did not get')
    return redirect('/questions')

