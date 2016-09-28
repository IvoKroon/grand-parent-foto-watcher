from django.shortcuts import render
from django.template import Context
from database.models import User
from users.forms import LoginForm, UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import *


# Create your views here.
def index(request):
    password = "niks1234"
    passw = make_password(password)
    # passw = 'bcrypt_sha256$$2b$12$hYg64qk24Y5ccDXWWfywE.VVm22JDq8tTG5v1Ds'
    passw = 'bcrypt_sha256$$2b$12$SgtLJcf/KzH7xLFvBgQHGuDNI2uB3995cUiPtQekuZk1.4irVmzEi'

    return render(request, 'home/index.html', Context({"password": passw, "check": check_password('niks1234', passw)}))
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
            email = form.cleaned_data['email']
            if check_email_exist(email):
                password = form.cleaned_data['password']
                user = User.objects.get(email=email)
                user_password = user.password

                if check_password(password, user_password):
                    # TODO make session.
                    # TODO Go to home of admin page.
                    request.session['user_id'] = user.id
                    return HttpResponseRedirect('/thanks/')

    return HttpResponseRedirect('/error/')


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = User()
            email = form.cleaned_data['email']

            if check_email_exist(email) is False:
                user.name = form.cleaned_data['name']
                user.lastName = form.cleaned_data['lastName']
                user.email = form.cleaned_data['email']
                user.password = make_password(form.cleaned_data['password'])
                user.member_id = 1
                user.save()
                return HttpResponseRedirect('/thanks/')

    return HttpResponseRedirect('/error/')


# check if emailaddress already exists?
def check_email_exist(email):
    num_results = User.objects.filter(email=email).count()
    if num_results == 0:
        return False
    else:
        return True


def home(request):
    user_id = request.session['user_id']
    user = User.objects.get(pk=user_id)
    c = Context({"user": user})
    return render(request, 'home/index.html', c)


def thanks(request):
    return render(request, 'success/index.html')


def error(request):
    return render(request, 'error/index.html')

