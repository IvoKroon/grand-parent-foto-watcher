from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.views import auth_check
from django.template import Context
from photo import ImageUploader
from photo.forms import PhotoForm
from database.models import Photos


def photo_page(request):
    auth_check(request)
    c = Context({'form': PhotoForm})
    return render(request, 'images/index.html', c)


def photo_home(request):
    auth_check(request)
    images = Photos.objects.all()
    c = Context({"images": images})
    return render(request, "images_home/index.html", c)


def image_uploading(request):
    if request.method == 'POST':
        # form = PhotoForm(request.POST)
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.session['user_id']
            up_image = form.cleaned_data['image']
            imager = ImageUploader.ImageUploader(image=up_image, user_id=user_id)
            print imager.get_amount_user_can_upload()
            if imager.upload():
                return HttpResponseRedirect('/thanks/')
    return HttpResponseRedirect('/error/')
