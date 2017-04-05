from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db.models import Q

from questions.forms import QuestionForm, AnswerForm
from .models import Question, Answer

from django.http import HttpResponseRedirect

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
            Q(tags__name__contains=query)|
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
    context = {'questions': reversed(Question.objects.all().order_by("votes")), 'tabs': 'most_votes'}
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
                tags = form.cleaned_data['tags'].split(",")

                user = User.objects.get(username=username)

                quest = Question.objects.create(title=title, body=body, user=user)

                #add tags one by one
                for tag in tags:
                    quest.tags.add(tag)


                # when you submit one question, you are redirected back to the main page
                return redirect('/questions')

            else:
                form = QuestionForm()

    return render(request, 'question_submission.html',{'form': form,})


@login_required(login_url='/login/')
def vote(request):
    print("********************")
    print("inne i vote Q")
    print("********************")
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
                #return render(request, "index.html", {'questions': Question.objects.all(), "href" :"/questions/vote?question={{ "+str(question.id)+" }}&votetype=up", 'this.queston.active_button': "True", 'id':question_id})
        else:
            print('ingen av delene')
    else:
        print('did not get')
    return redirect('/questions')

@login_required(login_url='/login/')
def answer_vote(request):
    print("********************")
    print("inne i vote answer")
    print("********************")
    user = request.user
    if request.method == "GET":
        answer_id = request.GET.get('answer', '')
        answer = Answer.objects.get(id=answer_id)
        if request.GET.get('votetype', '') == 'up':
            if answer.is_in_user_votes_up(user):
                pass
                print("Passed")

            else:
                answer.upvote_answer(user)
                print('upvoted')
                #return render(request, "index.html", {'questions': Question.objects.all(), "href" :"/questions/vote?question={{ "+str(question.id)+" }}&votetype=up", 'this.queston.active_button': "True", 'id':question_id})
        elif request.GET.get('votetype', '') == 'down':
            if answer.is_in_user_votes_down(user):
                pass
                print("Passed")

            else:
                answer.downvote_answer(user)
                print('upvoted')

    else:
        print('did not get')

    return redirect('/question')


@login_required(login_url='/login/')
def answers(request, question_id):
    # Could possibly use get_object_or_404 here
    question = Question.objects.get(pk = question_id)

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

    answers = reversed(Answer.objects.filter(answer_to=question).order_by('created_at'))
    context = {'question': question, 'answers': answers}  # Including one question and zero or more answers
    return render(request, 'answers.html', context, {'form': form, })

#    return redirect('/questions')



@login_required(login_url='/login/')
def myquestions(request):
    # makes a dictionary containing all Question objects
    # tabs:newest as default setting
    context = {'questions': Question.objects.filter(user = request.user), 'tabs':'newest', 'myQ':'true'}

    #search mechanism with Q lookups
    query = request.GET.get("q")
    if query:
        context = {'questions': Question.objects.filter(user=request.user).filter(
            Q(title__contains=query)|
                   Q(body__contains=query)).distinct()}
    # always needs to have a request, a go to html page and a dictrionary
    return render(request, 'index.html', context)

#Views for spørsmål sortert etter nyest og eldst
def myQnewest(request):
    # makes a dictionary containing all Question objects
    context = {'questions': reversed(Question.objects.filter(user = request.user)), 'tabs': 'newest', 'myQ':'true'}
    return render(request, 'index.html', context)

def myQoldest(request):
    context = {'questions': Question.objects.filter(user=request.user).order_by("created_at"), 'tabs':'oldest', 'myQ':'true'}
    return render(request, 'index.html', context)

def myQmost_votes(request):
    context = {'questions': reversed(Question.objects.all().order_by("votes")), 'tabs': 'most_votes'}
    return render(request, 'index.html', context)

def pinned(request):
    questions = Question.objects.filter(pinned_by=request.user)
    context = {'questions':questions, 'tabs': 'none'}
    return render(request, 'index.html', context)

def pin(request):
    user = request.user
    if request.method == "GET":
        question_id = request.GET.get('question', '')
        question = Question.objects.get(id=question_id)

        # Checking whether the user wants to pin or unpin
        if user in question.pinned_by.all():
            question.pinned_by.remove(user)
        else:
            question.pinned_by.add(user)
    else:
        print('did not get')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# view for tags
class TagIndexView(generic.ListView):
    template_name = 'index.html'
    model = Question
    paginate_by = 10
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.filter(tags__slug=self.kwargs.get('slug'))