from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.views import auth_check
from django.template import Context
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
            up_image = form.cleaned_data['image']
            imager = ImageUploader.ImageUploader(up_image)
            imager.upload()


            # print up_image.content_type
            # print up_image.name
            # print up_image.size
            # fs = FileSystemStorage('media/thumbnail')
            # filename = fs.save(up_image.name, up_image)
            # uploaded_file_url = fs.url(filename)
            # string_array = up_image.name.split('.')

            # print string_array


        else:
            print 'form not valid'

    return HttpResponseRedirect('/thanks/')
