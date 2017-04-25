from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

app_name = 'profilepage'

urlpatterns = [
    url(r'^$', views.index, name='index')

]
