from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.views import auth_check
from django.template import Context
import os.path
#
# from django.core.files.storage import FileSystemStorage
from photo import ImageUploader

from photo.forms import PhotoForm


def photo_page(request):
    if auth_check(request):
        c = Context({'form': PhotoForm})
        return render(request, 'images/index.html', c)
    else:
        return HttpResponseRedirect('/login/')


def image_upload(request):
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
