from django.shortcuts import render
from django.template import Context
from database.models import *
from users.forms import LoginForm, UserForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    return render(request, 'login/index.html')


def login(request):
    c = Context({"form": LoginForm})

    return render(request, 'login/index.html', c)


def register(request):
    c = Context({"form": UserForm})

    return render(request, 'register/index.html', c)


def create_user(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = User
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect('/thanks/')
        else:
            return HttpResponseRedirect('/error/')


def thanks(request):
    return render(request, 'success/index.html')


def error(request):
    return render(request, 'error/index.html')

