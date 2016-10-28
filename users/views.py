from django.shortcuts import render
from django.template import Context
from database.models import User, MemberShip
from users.forms import LoginForm, UserForm, RegistrationForm, UserProfileFrom
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import *
from django.contrib import messages
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.
def index(request):
    print "home"
    if auth_check(request):
        return HttpResponseRedirect("/slider/")
    else:
        return HttpResponseRedirect("/login/")


def login(request):
    if login_action(request):
        return HttpResponseRedirect("/home/")
    c = Context({"form": LoginForm})
    return render(request, 'login/index.html', c)


def register(request):
    # set the registration form
    reg_from = RegistrationForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        # check if the send form is valid
        if form.is_valid():
            user = User()
            email = form.cleaned_data['email']
            # check the the data in the form
            if check_email_exist(email) is False:
                if form.cleaned_data['name'] and form.cleaned_data['name'].strip():
                    if form.cleaned_data['lastName'] and form.cleaned_data['lastName'].strip():
                        if form.cleaned_data['email'] and form.cleaned_data['email'].strip():
                            # check if email is an email
                            try:
                                validate_email(form.cleaned_data['email'])
                            except ValidationError:
                                # show the error message
                                messages.error(request, 'Het emailadres is verkeerd!')
                                # fill back the form data
                                reg_from = RegistrationForm(initial={'name': form.cleaned_data['name'],
                                                                     'lastName': form.cleaned_data['lastName'],
                                                                     'email': form.cleaned_data['email']})

                                c = Context({"form": reg_from})
                                return render(request, 'register/index.html', c)

                            # if everything is true save the data
                            user.name = form.cleaned_data['name']
                            user.lastName = form.cleaned_data['lastName']
                            user.email = form.cleaned_data['email']
                            user.password = make_password(form.cleaned_data['password'])
                            user.member_id = 1
                            user.blocked = 0
                            user.save()
                            return HttpResponseRedirect("/login/")
            else:
                # The email address is already in use
                messages.error(request, 'Dit emailadres is al eens gebruikt!')
                reg_from = RegistrationForm(initial={'name': form.cleaned_data['name'],
                                                     'lastName': form.cleaned_data['lastName'],
                                                     'email': form.cleaned_data['email']})
    # There is no Post just load the page
    c = Context({"form": reg_from})
    return render(request, 'register/index.html', c)


def login_action(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            if check_email_exist(email):
                password = form.cleaned_data['password']
                user = User.objects.get(email=email)
                user_password = user.password

                if check_password(password, user_password):
                    request.session['user_id'] = user.id
                    request.session['membership'] = user.member.id
                    return True
                else:
                    messages.error(request, 'Foutief email of wachtwoord!')
                    return False
            else:
                messages.error(request, 'Foutief email of wachtwoord!')
                return False

        messages.error(request, 'Er is iets fout gegaan!')
    return False


def register_action(request):

    return HttpResponseRedirect("/error/")


def check_email_exist(email):
    num_results = User.objects.filter(email=email).count()
    if num_results == 0:
        return False
    else:
        return True


def logout(request):
    auth_check(request)
    del request.session['user_id']
    del request.session['membership']

    return HttpResponseRedirect("/login/")


def thanks(request):
    return render(request, 'success/index.html')


def success(request, success_id):
    switcher = {
        0: 'Je profiel gegevens zijn aangepast.',
        1: 'De foto is geupload.',
    }
    if int(success_id) in switcher:
        message = switcher[int(success_id)]
    else:
        message = 'Success'

    c = Context({'data': message})
    return render(request, 'success/index.html', c)


def error(request):
    return render(request, 'error/index.html')


def profile(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    form = UserProfileFrom(initial={'name': user.name, 'lastName': user.lastName, 'email': user.email})
    c = Context({"form": form, 'user': user})
    return render(request, 'profile/index.html', c)


def edit_user(request):
    if request.method == 'POST':
        form = UserProfileFrom(request.POST)
        if form.is_valid():
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            user.name = form.cleaned_data['name']
            user.lastName = form.cleaned_data['lastName']
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'Je hebt je profiel aangepast.')
            return HttpResponseRedirect('/user/profile/')
    return HttpResponseRedirect('/error/')


def auth_check(request):

    if 'user_id' in request.session:
        return True
    else:
        return False


# this is a function for the admin
# TODO ban users.
def users(request):
    if request.method == "POST":
        question = request.POST['question']
        if not question == "":
            if "options" in request.POST:
                option = request.POST.getlist('options')
            else:
                option = '0'

            print option
            filtering = []

            # filter[my_keyword] =
            # user_list = User.objects.filter(Q(name__icontains=question))
            # user_list.filter(Q(lastName__icontains=question))
            # user_list = User.objects.filter(Q(**filtering))

            if '0' in option:
                filtering.append({"name__icontains": question})
                filtering.append({"lastName__icontains": question})
                filtering.append({"email__icontains": question})
            if '2' in option:
                # user_list.filter(email__icontains=question)
                filtering.append({"name__icontains": question})

            if '3' in option:
                # user_list.filter(name__icontains=question)
                filtering.append({"lastName__icontains": question})

            if '1' in option:
                # user_list.filter(lastName__icontains=question)
                filtering.append({"email__icontains": question})
            print filtering[0]

            if len(filtering) == 1:
                user_list = User.objects.filter(Q(**filtering[0]))
            elif len(filtering) == 2:
                user_list = User.objects.filter(Q(**filtering[0]) | Q(**filtering[1]))
            elif len(filtering) == 3:
                print "JAJA"
                user_list = User.objects.filter(Q(**filtering[0]) | Q(**filtering[1]) | Q(**filtering[2]))

            if user_list.count() == 0:
                messages.error(request, 'Er is niks gevonden.')

            c = Context({"users": user_list})
            print user_list
            return render(request, "admin_users/index.html", c)
        else:
            messages.error(request, 'Er is niks gevonden.')
            c = Context({"users": None})
            return render(request, "admin_users/index.html", c)

    return render(request, 'admin_users/index.html')


