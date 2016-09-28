from django.shortcuts import render
from django.template import Context
from database.models import User
from users.forms import LoginForm, UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import *


# Create your views here.
def index(request):
    # password = "password"
    passw = make_password("password")


    return render(request, 'home/index.html', Context({"password": passw, "check": }))



def login(request):

            # c = Context({"form": LoginForm})
            # Entry.objects.get(pk=1)
            # user = User.objects.get(email)
            # check_password(password, hash)
            return render(request, 'login/index.html', c)


def register(request):
    c = Context({"form": UserForm})

    return render(request, 'register/index.html', c)


def check_user(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

def create_user(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = User()
            user.name = form.cleaned_data['first_name']
            user.lastName = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect('/thanks/')
        else:
            return HttpResponseRedirect('/error/')


def thanks(request):
    return render(request, 'success/index.html')


def error(request):
    return render(request, 'error/index.html')

