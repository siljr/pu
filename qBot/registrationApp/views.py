from django.shortcuts import render

# Create your views here.
from registrationApp.forms import *

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response



def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            return HttpResponseRedirect('/')
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registrationApp/register.html',variables)