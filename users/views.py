from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from database.models import *


# Create your views here.
def index(request):
    return render(request, 'login/index.html')
