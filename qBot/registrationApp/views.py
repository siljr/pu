from django.shortcuts import render

# Create your views here.
from registrationApp.forms import *

from django.http import HttpResponseRedirect
from django.shortcuts import render


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            return HttpResponseRedirect('/questions')
    form = RegistrationForm()
    context = {'form': form}
    return render(request, 'registrationApp/register.html', context)
