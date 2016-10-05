from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.views import auth_check
from django.template import Context
from slider.forms import SliderForm
from database.models import Slides, Background, User


def home(request):
    auth_check(request)
    user = User.objects.get(id=request.session['user_id'])
    sliders = Slides.objects.filter(user=user)
    c = Context({'sliders': sliders})
    return render(request, 'slider_home/index.html', c)


def detail(request):
    auth_check(request)

    return render(request, 'slider_detail/index.html')


def create_page(request):
    auth_check(request)
    c = Context({
        "form": SliderForm
    })

    return render(request, "slider_create/index.html", c)


def create(request):
    auth_check(request)
    if request.method == 'POST':
        form = SliderForm(request.POST)

        if form.is_valid():
            # make new slider
            slider = Slides()
            slider.title = form.cleaned_data['title']
            slider.desc = form.cleaned_data['desc']
            slider.speed = form.cleaned_data['speed']
            slider.background = Background.objects.get(id=1)
            slider.save()
            # Set the many to many relation
            user = User.objects.get(id=request.session['user_id'])
            slider.user.add(user)

            return HttpResponseRedirect('/thanks/')

    return HttpResponseRedirect('/error/')


