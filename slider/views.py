from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.views import auth_check
from django.template import Context


def create_slider(request):
    auth_check(request)

    return render(request, "slider_home/index.html")
