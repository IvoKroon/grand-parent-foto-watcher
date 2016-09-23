from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context

from database.models import *
from base.functions.randomHash import *


def index(request):

    # c = Context({
    #     'data': User.objects.all(),
    # })

    c = Context({
        'data': User.objects.all(),
        'hash': RandomHash.generate(),
    })

    # add new user
    # u = User(name="Ivo", lastName="Kroon", email="ivokroo@gmail.com", member_id=1)
    # u.save()

    # m = MemberShip(title="free", kind=1)
    # m.save()
    # m = MemberShip(title="starter", kind=2)
    # m.save()
    # m = MemberShip(title="premium", kind=3)
    # m.save()

    return render(request, 'login/index.html', c)
