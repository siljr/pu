from django.conf.urls import url

from . import views

app_name = 'questions'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^$', views.questions, name='questions'),
    url(r'create_question', views.register_question, name='create_question'),
    url(r'^(?P<question_id>\d+)/$', views.answers, name='answers')
]
