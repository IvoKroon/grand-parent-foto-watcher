from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from database.models import *

# Create your views here.
def index(request):
    user = User.objects.all()

    c = Context({
        'data': user,
    })

    # u = User(name="lotte", lastName="de korte", email="ivokroo@gmail.com", member_id=2)
    # u.save()
    return render(request, 'login/index.html', c)
