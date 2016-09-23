from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context


def index(request):

    return render(request, 'login/index.html')
