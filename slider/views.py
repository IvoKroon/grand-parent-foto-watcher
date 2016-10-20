from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from users.views import auth_check
from django.template import Context
from slider.forms import SliderForm
from database.models import Slides, Background, User, Photos
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    user = User.objects.get(id=request.session['user_id'])
    # sliders = Slides.objects.filter(user=user).all()
    # articles = Article.objects.filter(tags__in=[2])
    # sliders = Slides.objects.filter(user=user)

    # slider = Slides.objects.filter()
    Photos.objects.filter()
    slides = Slides.objects.filter(user=user)
    sliders = []
    for slide in slides:
        photo = Photos.objects.filter(slides=slide).first()

        # slide.photo = photo
        sliders.append({'slide': slide, 'photo': photo})

    c = Context({'sliders': sliders})
    # c = Context()
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
            slider.save()
            # Set the many to many relation
            user = User.objects.get(id=request.session['user_id'])
            slider.user.add(user)

            return HttpResponseRedirect('/thanks/')

    return HttpResponseRedirect('/error/')


def add_image_to_slider(request, slider_id):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    # todo do not show images that are already selected.
    images = Photos.objects.filter(user=User.objects.get(id=request.session['user_id']))
    images = images.exclude(slides=Slides.objects.get(id=slider_id))

    c = Context({"images": images, "slider_id": slider_id})

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
    num_results = Slides.objects.filter(id=slider_id).filter(user=User.objects.get(id=request.session['user_id'])).count()
    print num_results
    if num_results == 0:
        return False
    else:
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
