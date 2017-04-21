from django.conf.urls import url

from . import views

app_name = 'questions'

urlpatterns = [
    # base urls for all questions and for creating a new question
    url(r'^$', views.index, name='index'),
    url(r'create_question', views.register_question, name='create_question'),

    # urls for single questions
    url(r'^(?P<question_id>\d+)/$', views.answers, name='answers'),
    url(r'vote', views.vote, name='register_vote'),
    url(r'1234', views.answer_vote, name='register_answ'),

    # urls for sorting all questions
    url(r'newest/$', views.newest, name="newest"),
    url(r'oldest/$', views.oldest, name="oldest"),
    url(r'popular/$', views.most_votes, name="most_votes"),

    # urls for my questions
    url(r'myquestions/$', views.myquestions, name="myquestions"),
    url(r'myquestions/n/$', views.myQnewest, name="myQnewest"),
    url(r'myquestions/o/$', views.myQoldest, name="myQoldest"),
    url(r'myquestions/mv/$', views.myQmost_votes, name="myQmost_votes"),

    # urls for pinning/favourite
    url(r'pin/$', views.pin, name="pin"),
    url(r'pinned/$', views.pinned, name="pinned"),

    # urls for tags
    url(r'tag/(?P<slug>\w+)/$', views.TagIndexView.as_view(), name='tagged')
]
