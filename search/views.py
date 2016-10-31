from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from users.views import auth_check
from django.template import Context
from database.models import Photos, User, Slides
from django.db.models import Q
from django.core import serializers
from django.db.models import Count


def search(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    if request.method == "POST":
        slider = search_slider(request)
        c = Context({"slider": slider})
        return render(request, 'search_home/index.html', c)
    return render(request, 'search_home/index.html')


def search_slider(request):
    search_tag = request.POST['search']
    user = User.objects.get(id=request.session['user_id'])
    if request.session['membership'] == 3:
        # slides = Slides.objects.filter(Q(title__icontains=search_tag) | Q(hash=search_tag))
        # get slides and count the amount of views.
        slides = Slides.objects.annotate(views_count=Count('views')).filter(
            Q(title__icontains=search_tag) | Q(hash=search_tag))
    else:
        slides = Slides.objects.annotate(views_count=Count('views')).filter(
            Q(title__icontains=search_tag) | Q(hash=search_tag)).filter(user=user)
    sliders = []
    for slide in slides:
        photo = Photos.objects.filter(slides=slide).first()
        sliders.append({'slide': slide, 'photo': photo})
    return sliders


def search_action(request):
    if request.method == "POST":
        search_tag = request.POST['search']
        slider = Slides.objects.filter(Q(title__contains=search_tag) | Q(hash=search_tag))
        data = serializers.serialize('json', slider)
        return JsonResponse(data)
    return JsonResponse({"error": "We need a Post here!"})

