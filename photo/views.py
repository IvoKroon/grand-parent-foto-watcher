from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from users.views import auth_check
from django.template import Context
from photo import ImageUploader
from photo.forms import PhotoForm
from database.models import Photos, User
from django.core.exceptions import ObjectDoesNotExist


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
        user_id = request.session['user_id']
        up_image = request.FILES.getlist('image')
        # title = form.cleaned_data['title']
        # desc = form.cleaned_data['desc']
        image_upload = ImageUploader.ImageUploader()
        for image in up_image:
            print image.name
            image_upload.upload(image, image.name, user_id)

        return HttpResponseRedirect('/images/')
    return HttpResponseRedirect('/error/')


def check_image_by_id(request, image_id):
    try:
        Photos.objects.filter(user=User.objects.get(id=request.session['user_id'])).get(id=image_id)
        return True
    except ObjectDoesNotExist:
        return False


def image_remove_ajax(request):
    if not auth_check(request):
        return JsonResponse({"error": "No auth!"})

    # return JsonResponse({'test': request.POST['image_id']})
    if request.method == 'POST':
        image_id = request.POST['image_id']
        if image_id.isdigit():
            user_id = request.session['user_id']
            ImageUploader.ImageUploader().remove(image_id,user_id)
            return JsonResponse({"success": "The photo is removed"})
    return JsonResponse({"error": "Error"})




