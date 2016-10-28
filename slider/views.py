from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from users.views import auth_check
from django.template import Context
from slider.forms import SliderForm, CodeFrom
from database.models import Slides, Background, User, Photos, Views
from django.core.exceptions import ObjectDoesNotExist
from base.functions.randomHash import RandomHash
from django.contrib import messages
from django.db.models import Count


def home(request):
    if not auth_check(request):
        return HttpResponseRedirect("/login/")

    user = User.objects.get(id=request.session['user_id'])
    if request.session['membership'] is not 3:
        # get slides and count the amount of views.
        slides = Slides.objects.annotate(views_count=Count('views')).filter(user=user)
    else:
        slides = Slides.objects.filter()

    sliders = []
    for slide in slides:
            photo = Photos.objects.filter(slides=slide).first()
            sliders.append({'slide': slide, 'photo': photo})
    if slides.count() == 0:
        c = Context({'sliders': None})
    else:
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
                user = User.objects.get(id=user_id)

                slider = Slides.objects.prefetch_related("photo").filter(id=slider_id).filter(user=user)

                photos = slider[0].photo.values()

                c = Context({"slider": slider[0], "photos": photos})
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

    # This bool is to check if there is a photo uploaded.
    uploaded = True
    images = Photos.objects.filter(user=User.objects.get(id=request.session['user_id']))
    if images.count() == 0:
        uploaded = False

    images = images.exclude(slides=Slides.objects.get(id=slider_id))
    slider = Slides.objects.get(id=slider_id)

    c = Context({"images": images, "slider": slider, "uploaded":uploaded})

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


def slider_shower(request, slide_hash):
    try:
        slider = Slides.objects.get(hash=slide_hash)

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/slider/show_error')

    if slider.active == 0:
        # Todo built view controller
        slide_id = get_slider_id_by_hash(request, slide_hash)
        if 'views' in request.session:
            viewed = request.session['views']
            if slide_id not in viewed:
                views = Views()
                views.slider_id = Slides.objects.get(id=slide_id)
                views.ip = "0.0.0.0"
                views.save()
                viewed.append(slide_id)
                request.session['views'] = viewed
        else:
            views = Views()
            views.slider_id = Slides.objects.get(id=slide_id)
            views.ip = "0.0.0.0"
            viewed = [slide_id]
            views.save()
            request.session['views'] = viewed

        images = Photos.objects.filter(slides=slider)
        c = Context({'remove_header': True, 'slider': slider, 'images': images, 'amount': get_views(request, slide_id)})
        add_viewer(request)
        return render(request, "slider_show/index.html", c)
    else:
        return HttpResponseRedirect('/slider/slider_offline')


def get_views(request, slider_id):
    views = Views.objects.filter(slider_id=Slides.objects.get(id=slider_id)).count()
    if views >= 3:
        slides = Slides.objects.prefetch_related("user").get(id=slider_id)
        user = slides.user
        u_id = user.values_list('id', flat=True)
        user = User.objects.get(id=u_id)
        if user.member_id == 1:
            user.member_id = 2
            user.save()

    return views


def get_slider_id_by_hash(request, slider_hash):
    try:
        slides = Slides.objects.get(hash=slider_hash)
        return slides.id
    except ObjectDoesNotExist:
        return False


def add_viewer(request):
    print get_client_ip(request)
    return True


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def slider_show_error(request):
    return render(request, 'slider_show_error/index.html')


def slider_show_offline(request):
    return render(request, 'slider_show_error/slider_offline.html')


def edit(request, slider_id):
    if check_slider_belongs_user(slider_id, request) is False:
        return HttpResponseRedirect("/slider/")

    slider = Slides.objects.get(id=slider_id)
    form = SliderForm(initial={'title': slider.title, 'desc': slider.desc, 'speed': slider.speed})
    c = Context({'slider': slider, 'form': form})
    return render(request, 'slider_edit/index.html', c)


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
            messages.success(request, 'Je profiel is aangepast!')
            return HttpResponseRedirect(link)
    return HttpResponseRedirect('/error/')


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

