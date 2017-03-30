"""qBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from questions import views
from registrationApp import views as registration_views
from questions import views as question_views
from django.views.generic import TemplateView

urlpatterns = [
    # makes sure the url file from questions is added. Namespace allows us to call "questions:name"
    url(r'^questions/', include('questions.urls', namespace="questions")),
    url(r'^$', question_views.index, name='index'),

    #myquestions
    #url(r'^myquestions/$', views.MyqView.as_view(), name="my_questions"),

    # adding all the urls from the qbot main app
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),

    # adding urls from the registrationApp
    url(r'^register', registration_views.register_page, name='registerpage'),

    # adding admin page (default)
    url(r'^admin/', admin.site.urls),

    # adding about page
    url(r'^about/', TemplateView.as_view(template_name='about_us.html')),
]
