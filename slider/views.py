from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from users.views import auth_check
from django.template import Context
from slider.forms import SliderForm, CodeFrom
from database.models import Slides, Background, User, Photos
from django.core.exceptions import ObjectDoesNotExist
from base.functions.randomHash import RandomHash


def home(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    user = User.objects.get(id=request.session['user_id'])
    if request.session['membership'] is not 3:
        slides = Slides.objects.filter(user=user)
    else:
        slides = Slides.objects.filter()

    sliders = []
    for slide in slides:
            photo = Photos.objects.filter(slides=slide).first()
            sliders.append({'slide': slide, 'photo': photo})
    c = Context({'sliders': sliders})
    return render(request, 'slider_home/index.html', c)


def detail(request, slider_id):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")
    # print slider_id
    if request.method == 'GET':
        if slider_id and slider_id != "":
            try:
                user_id = request.session['user_id']
                # slider = Slides.objects.get(id=slider_id)
                user = User.objects.get(id=user_id)
                slider = Slides.objects.filter(user=user).get(id=slider_id)
                images = Photos.objects.filter(slides=slider_id)
                c = Context({"slider": slider, "images": images})
                return render(request, 'slider_detail/index.html', c)
            except ObjectDoesNotExist:
                print "error"
                return HttpResponseRedirect('/error/')

    return HttpResponseRedirect('/error/')


def create_page(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")
    c = Context({
        "form": SliderForm
    })

    return render(request, "slider_create/index.html", c)


def create(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")
    if request.method == 'POST':
        form = SliderForm(request.POST)

        if form.is_valid():
            # make new slider
            slider = Slides()
            slider.title = form.cleaned_data['title']
            slider.desc = form.cleaned_data['desc']
            slider.speed = form.cleaned_data['speed']
            slider.background = Background.objects.get(id=1)
            slider.active = 0
            slider.hash = RandomHash().generate(5)
            slider.save()

            # Set the many to many relation
            user = User.objects.get(id=request.session['user_id'])
            slider.user.add(user)
            slider_id = slider.id
            link = '/slider/detail/' + str(slider_id)
            return HttpResponseRedirect(link)

    return HttpResponseRedirect('/error/')


def add_image_to_slider(request, slider_id):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    # todo do not show images that are already selected.
    images = Photos.objects.filter(user=User.objects.get(id=request.session['user_id']))
    images = images.exclude(slides=Slides.objects.get(id=slider_id))
    slider = Slides.objects.get(id=slider_id)

    c = Context({"images": images, "slider": slider})

    return render(request, "slider_add_images/index.html", c)


def add_image(request, slider_id):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")
    # Get all posted images and add these to the slider
    selected_images = request.POST.getlist('selected_photos')
    slider = Slides.objects.get(id=slider_id)
    for image_id in selected_images:
        slider.photo.add(image_id)

    slider.save()

    return HttpResponseRedirect("/slider/detail/" + slider_id)


# ajax calls
def remove_image_from_slider(request, slider_id, image_id):
    if not auth_check(request):
        return JsonResponse({'error': 'No auth found'})

    try:
        # check if the user has the selected slider
        if check_slider_belongs_user(slider_id, request):
            Slides.objects.get(id=slider_id).photo.remove(Photos.objects.get(id=image_id))
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': "No slider found"})

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Exception'})


def check_slider_belongs_user(slider_id, request):
    # When the admin is online always show True
    if request.session['membership'] == 3:
        return True

    slides = Slides.objects.filter(id=slider_id)\
        .filter(user=User.objects.get(id=request.session['user_id']))

    if slides.count() is 0:
        print False
        return False
    else:
        print True
        return True


def switch_slider_status(request):
    if not auth_check(request):
        return JsonResponse({'error': 'No auth found'})

    if request.method == 'POST':
        state = request.POST['status']
        slider_id = request.POST['slider_id']
        if "status" in request.POST and "slider_id" in request.POST:
            try:
                slider = Slides.objects.get(id=slider_id)
                slider.active = state
                slider.save()
                return JsonResponse({"success": True})
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Exception error"})
        else:
            return JsonResponse({"error": "Not the right post request send"})

    return JsonResponse({"error": "No Post found!"})


def slider_shower(request, hash):
    try:
        slider = Slides.objects.get(hash=hash)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/slider/show_error')

    if slider.active == 0:
        images = Photos.objects.filter(slides=slider)
        c = Context({'remove_header': True, 'slider': slider, 'images': images})
        return render(request, "slider_show/index.html", c)

    return HttpResponseRedirect('/slider/show_error')


def slider_show_error(request):
    return render(request, 'slider_show_error/index.html')


def edit_action(request, slider_id):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    if not check_slider_belongs_user(slider_id, request):
        HttpResponseRedirect("/sliders/")

    if request.method == 'POST':
        form = SliderForm(request.POST)
        if form.is_valid():
            # slider_id = request.POST['slider_id']
            slider = Slides.objects.get(id=slider_id)
            slider.title = form.cleaned_data['title']
            slider.desc = form.cleaned_data['desc']
            slider.speed = form.cleaned_data['speed']
            slider.save()
            link = '/slider/edit/'+slider_id
            return HttpResponseRedirect(link)
    return HttpResponseRedirect('/error/')


def edit(request, slider_id):
    if check_slider_belongs_user(slider_id, request) is False:
        # print ''
        return HttpResponseRedirect("/slider/")

    slider = Slides.objects.get(id=slider_id)
    form = SliderForm(initial={'title': slider.title, 'desc': slider.desc, 'speed': slider.speed})
    c = Context({'slider': slider, 'form': form})
    return render(request, 'slider_edit/index.html', c)


def remove_action(request, slider_id):
    if not check_slider_belongs_user(slider_id, request):
        return HttpResponseRedirect("/slider/")

    if request.method == 'POST':
        slider = Slides.objects.get(id=slider_id)
        slider.delete()
        return HttpResponseRedirect('/slider/')
    return HttpResponseRedirect('/error/')


def share(request, slider_id):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    if not check_slider_belongs_user(slider_id, request):
        return HttpResponseRedirect("/slider/")

    slider = Slides.objects.get(id=slider_id)

    c = Context({"slider": slider})

    return render(request, 'slider_share/index.html', c)


def code(request):
    c = Context({"form": CodeFrom})
    return render(request, 'slider_code/index.html', c)


def code_action(request):
    if request.method == 'POST':
        form = CodeFrom(request.POST)
        if form.is_valid():
            code = form

