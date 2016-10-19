from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.views import auth_check
from django.template import Context
from photo import ImageUploader
from photo.forms import PhotoForm
from database.models import Photos, User


def photo_page(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    auth_check(request)
    c = Context({'form': PhotoForm})
    return render(request, 'images/index.html', c)


def photo_home(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    user = User.objects.get(id=request.session['user_id'])
    images = Photos.objects.filter(user=user)
    c = Context({"images": images})
    return render(request, "images_home/index.html", c)


def image_uploading(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.session['user_id']
            up_image = form.cleaned_data['image']
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            image_upload = ImageUploader.ImageUploader(image=up_image, user_id=user_id, title=title, desc=desc)

            if image_upload.upload():
                return HttpResponseRedirect('/images/')
    return HttpResponseRedirect('/error/')
