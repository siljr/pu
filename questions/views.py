from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q
from questions.forms import QuestionForm, AnswerForm
from .models import Question, Answer
from django.http import HttpResponseRedirect


@login_required(login_url='/login/')
def index(request):
    # makes a dictionary containing all Question objects
    # tabs:newest as default setting
    context = {'questions': reversed(Question.objects.all()), 'tabs': 'newest'}

    # search mechanism with Q lookups
    query = request.GET.get("q")
    if query:
        context = {'questions': Question.objects.filter(
            Q(title__contains=query) |
            Q(tags__name__contains=query) |
            Q(body__contains=query)).distinct()}
    # always need to have a request, a go to html page and a dictionary
    return render(request, 'index.html', context)


# Views for questions sorted by time or votes
def newest(request):
    # makes a dictionary containing all Question objects
    context = {'questions': reversed(Question.objects.all().order_by("created_at")), 'tabs': 'newest'}
    return render(request, 'index.html', context)


def oldest(request):
    context = {'questions': Question.objects.all().order_by("created_at"), 'tabs': 'oldest'}
    return render(request, 'index.html', context)


def most_votes(request):
    context = {'questions': reversed(Question.objects.all().order_by("votes")), 'tabs': 'most_votes'}
    return render(request, 'index.html', context)


@login_required(login_url='/login/')
def register_question(request):
    form = QuestionForm()

    if request.method == "POST":
        form = QuestionForm(request.POST)

        if request.user.is_authenticated():
            username = request.user.username

            if form.is_valid():
                # Fetching data form the form when submitted
                title = form.cleaned_data['title']
                body = form.cleaned_data['body']
                tags = form.cleaned_data['tags']
                user = User.objects.get(username=username)

                # Creating a question with the collected data
                quest = Question.objects.create(title=title, body=body, user=user)

                # Adding tags one by one
                if tags:
                    if "," in tags:
                        t = tags.split(",")
                        for tag in t:
                            quest.tags.add(tag)
                    else:
                        t =tags.split(" ")
                        for tag in t:
                            quest.tags.add(tag)

                # After submitting a question you are redirected back to the main page
                return redirect('/questions')
            else:
                form = QuestionForm()

    return render(request, 'question_submission.html', {'form': form, })


@login_required(login_url='/login/')
def vote(request):
    user = request.user

    if request.method == "GET":
        question_id = request.GET.get('question', '')
        question = Question.objects.get(id=question_id)

        if request.GET.get('votetype', '') == 'up':

            if question.is_in_user_votes(user):     #The user has already voted up
                question.downvote_question(user)    #The upvote will be removed (hence downvote)
                question.button_list.remove(user)   #Removes the user from active button list
            else:
                question.upvote_question(user)      #Upvotes question
                question.button_list.add(user)      #Adds the user to upvote list

    return redirect('/questions')


@login_required(login_url='/login/')
def answer_vote(request):
    user = request.user

    if request.method == "GET":
        answer_id = request.GET.get('answer', '')
        answer = Answer.objects.get(id=answer_id)

        if request.GET.get('votetype', '') == 'up':

            if answer.is_in_user_votes_up(user):            #If user already has voted up
                answer.downvote_regret(user)                #Vote answer down
                answer.button_up.remove(user)               #Remove user from active button list
            else:
                if answer.is_in_user_votes_down(user):      #If user already has voted down
                    answer.button_down.remove(user)         #Remove user form downvote list

                answer.upvote_answer(user)                  #Upvote answer
                answer.button_up.add(user)                  #Add the user to upvote list

        elif request.GET.get('votetype', '') == 'down':     #Same as request = 'up' only opposite.

            if answer.is_in_user_votes_down(user):
                answer.upvote_regret(user)
                answer.button_down.remove(user)
            else:
                if answer.is_in_user_votes_up(user):
                    answer.button_up.remove(user)

                answer.downvote_answer(user)
                answer.button_down.add(user)

    question_id = request.GET.get('question', '')
    return redirect('/questions/'+str(question_id))

# View for a single question with/wo answers and a possibility to create an answer
@login_required(login_url='/login/')
def answers(request, question_id):

    question = Question.objects.get(pk=question_id)
    form = AnswerForm()
    if request.method == "POST":
        form = AnswerForm(request.POST)

        if request.user.is_authenticated():
            username = request.user.username

            if form.is_valid():
                # Fetching data for the answer
                body = form.cleaned_data['body']
                user = User.objects.get(username=username)

                # Creating the answer object
                Answer.objects.create(body=body, user=user, answer_to=question)
                # No redirecting, just refreshing same page.
            else:
                form = AnswerForm()

    answers = reversed(Answer.objects.filter(answer_to=question).order_by('created_at'))
    context = {'question': question, 'answers': answers, 'myanswers': Answer.objects.filter(user=request.user) }  # Including one question and zero or more answers
    return render(request, 'answers.html', context, {'form': form, })


# Views for "my questions". Sorted by newest, oldest and most votes
# "myQ" marks whether the user is in my questions or not. Used further in links in html files.
# "tabs" marks the active tab for the html files.

@login_required(login_url='/login/')
def myquestions(request):
    # makes a dictionary containing all Question objects
    # tabs:newest as default setting
    context = {'questions': Question.objects.filter(user=request.user), 'tabs':'newest', 'myQ':'true'}

    # search mechanism with Q lookups
    query = request.GET.get("q")
    if query:
        context = {'questions': Question.objects.filter(user=request.user).filter(
            Q(title__contains=query)|
                   Q(body__contains=query)).distinct()}
    # always needs to have a request, a go to html page and a dictionary
    return render(request, 'index.html', context)


def myQnewest(request):
    # makes a dictionary containing all Question objects
    context = {'questions': reversed(Question.objects.filter(user=request.user)), 'tabs': 'newest', 'myQ': 'true'}
    return render(request, 'index.html', context)


def myQoldest(request):
    context = {'questions': Question.objects.filter(user=request.user).order_by("created_at"), 'tabs': 'oldest', 'myQ': 'true'}
    return render(request, 'index.html', context)


def myQmost_votes(request):
    context = {'questions': reversed(Question.objects.all().order_by("votes")), 'tabs': 'most_votes', 'myQ': 'true'}
    return render(request, 'index.html', context)


def pinned(request):
    # Getting the questions pinned by the user making the request
    questions = Question.objects.filter(pinned_by=request.user)
    context = {'questions': questions, 'tabs': 'none'}
    return render(request, 'index.html', context)


def pin(request):
    user = request.user
    if request.method == "GET":
        # Getting the question that has been clicked on
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
    # paginate_by = 10
    context_object_name = 'questions'

    def get_queryset(self):
        return Question.objects.filter(tags__slug=self.kwargs.get('slug'))


def scores(request):
    users = User.objects.all().order_by("username")
    u_scores = []
    for user in users:
        u_answers = Answer.objects.filter(user=user)
        score = 0
        for answer in u_answers:
            score += answer.votes
        u_scores.append(score)
    lists = zip(users, u_scores)
    context = {'lists': lists}
    return render(request, 'scores.html', context)