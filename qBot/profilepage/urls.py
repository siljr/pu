from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

app_name = 'profilepage'

urlpatterns = [
    url(r'^$', views.index, name='index')
    #url(r'create_question', views.register_question, name='create_question'),
]