from django.conf.urls import url

from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'create_question', views.register_question, name='create_question'),
    url(r'vote', views.vote, name='register_vote'),
    url(r'(?P<question_id>\d+)/answer_vote', views.answer_vote, name='register_answer'),
    url(r'^(?P<question_id>\d+)/$', views.answers, name='answers'),
    url(r'newest/$', views.newest, name="newest"),
    url(r'oldest/$', views.oldest, name="oldest"),
    url(r'popular/$', views.most_votes, name="most_votes"),
    # url(r'most_votes/$', views.most_votes, name="most_votes"),
    url(r'myquestions/$', views.myquestions, name="myquestions"),
    url(r'myquestions/n/$', views.myQnewest, name="myQnewest"),
    url(r'myquestions/o/$', views.myQoldest, name="myQoldest"),
    url(r'myquestions/mv/$', views.myQmost_votes, name="myQmost_votes"),
    url(r'pin/$', views.pin, name="pin"),
    url(r'pinned/$', views.pinned, name="pinned"),
    url(r'tag/(?P<slug>\w+)/$', views.TagIndexView.as_view(), name='tagged')
]
