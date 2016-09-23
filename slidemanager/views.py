from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# from slidemanager.functions.randomHash import *
# from database.models import *


# Create your views here.
def index(request):
    # # t = loader.get_template('templates/detail/index.html')
    # # u = User.objects.all()
    #
    # # u = User.objects.all().id
    #
    # r = RandomHash.generate()
    # c = Context({
    #     'data': User.objects.all(),
    #     'code': r,
    #     'amount': len(r)
    # })
    # # m = MemberShip.objects.get(pk=1)
    # # u = User(name="Ivo", lastName="kroon", email="ivokroo@gmail.com", member_id=2)
    # # u.save()
    # return render(request, 'detail/index.html')

    return render(request, 'detail/index.html')


def create(request):
    if request.method == 'POST':
        # u = User(name="Ivo", lastName="kroon", email="ivokroo@gmail.com", member_id=2)
        # u.save()
        return HttpResponseRedirect('/success/')


def detail(request):
    p = PhotoUploader().showing("test")

    return HttpResponse(p)


def success(request):
    return render(request, 'success/index.html')

