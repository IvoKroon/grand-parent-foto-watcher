from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import Context
from guest.forms import GuestForm
from database.models import Slides
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def index(request):
    if request.method == "POST":
        print "POST"
        form = GuestForm(request.POST)
        if form.is_valid():
            slider_hash = form.cleaned_data['code']
            if check_if_slider_exist(request, slider_hash):
                print "FORM VALId"
                print "GO"
                slider_hash = form.cleaned_data['code']
                url = "/slider/show/" + slider_hash + "/"
                return HttpResponseRedirect(url)
            else:
                messages.error(request, "De hash klopt niet!")
        else:
            print "Not valid"

    form = GuestForm()
    c = Context({"form": form})
    return render(request, "guest_home/index.html", c)


def check_if_slider_exist(request, slider_hash):
    try:
        Slides.objects.get(hash=slider_hash)
        return True
    except ObjectDoesNotExist:
        return False
