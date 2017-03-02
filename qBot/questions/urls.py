from django.conf.urls import url

from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^$', views.questions, name='questions'),
    url(r'create_question', views.register_question, name='create_question'),
    url(r'newest/$', views.newest, name="newest"),
    url(r'oldest/$', views.oldest, name="oldest"),
    url(r'most_votes/$', views.most_votes, name="most_votes")

    # just a comment
]
