from django.shortcuts import render
from django.template import Context
from database.models import User
from users.forms import LoginForm, UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import *


# Create your views here.
def index(request):
    # password = "password"
    # passw = make_password("password")

    # return render(request, 'home/index.html', Context({"password": passw, "check": }))
    print check_email_exist("ivokroo@gmail.com")
    return render(request, 'home/index.html')


def login(request):
    # c = Context({"form": LoginForm})
    # Entry.objects.get(pk=1)
    # user = User.objects.get(email)
    # check_password(password, hash)
    c = Context({"form": LoginForm})
    return render(request, 'login/index.html',c)


def register(request):
    c = Context({"form": UserForm})

    return render(request, 'register/index.html', c)


def check_user(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # TODO Find user by email.
            # TODO Get password.
            # TODO Check password.
            # TODO make session.
            # TODO Go to home of admin page.

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.get(email=email)
            if user:
                user_password = user.password
                if check_password(password, user_password):

                    print(email + " " + password)
                    return HttpResponseRedirect('/thanks/')


def create_user(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # todo check if email is unique
            user = User()
            email = form.cleaned_data['email']

            if check_email_exist(email) is False:
                user.lastName = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.password = make_password(form.cleaned_data['password'])
                user.member_id = 1
                user.save()
                return HttpResponseRedirect('/thanks/')

            else:
                return HttpResponseRedirect('/error/')

        else:
            return HttpResponseRedirect('/error/')


def check_email_exist(email):

    # user = User.objects.get(email=email)
    num_results = User.objects.filter(email=email).count()
    if num_results == 0:
        return False
    else:
        return True


def thanks(request):
    return render(request, 'success/index.html')


def error(request):
    return render(request, 'error/index.html')

