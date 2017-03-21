from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.views import generic

from questions.forms import QuestionForm, AnswerForm
from .models import Question, Answer


@login_required(login_url='/login/')
def index(request):
    # makes a dictionary containing all Question objects
    context = {'questions': Question.objects.all()}
    # always needs to have a request, a go to html page and a dictionary
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




    return redirect('/questions')

class MyqView(generic.ListView):
    template_name = 'my_questions.html'
    context_object_name = 'my_questions'

    def get_queryset(self):
        return Question.objects.filter(user = self.request.user)

@login_required(login_url='/login/')
def answers(request, question_id):
    # Could possibly use get_object_or_404 here
    question = Question.objects.get(pk = question_id)
    answers = reversed(Answer.objects.filter(answer_to=question).order_by('created_at'))

    form = AnswerForm()
    if request.method == "POST":
        username = None
        form = AnswerForm(request.POST)
        if request.user.is_authenticated():
            username = request.user.username
            if form.is_valid():
                body = form.cleaned_data['body']

                user = User.objects.get(username=username)

                Answer.objects.create(body=body, user=user, answer_to=question)

                # No redirecting, just refreshing same page.

            else:
                form = AnswerForm()

    context = {'question': question, 'answers': answers}  # Including one question and zero or more answers
    return render(request, 'answers.html', context, {'form': form, })
