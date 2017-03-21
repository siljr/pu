from django.conf.urls import url

from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'create_question', views.register_question, name='create_question'),
    url(r'vote', views.vote, name='register_vote'),
]
