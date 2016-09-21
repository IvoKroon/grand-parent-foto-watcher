from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader


# Create your views here.
def index(request):
    # t = loader.get_template('templates/detail/index.html')
    c = Context({
        'stuff': 'you',
        'stuff2': 'the rocksteady crew',
        'other_content': "data",
    })

    return render(request, 'detail/index.html', c);
    # return render(request, 'users/index.html', context)
    # return HttpResponse("Hello photo app")


def detail(request):
    return HttpResponse("Hello photo app detail")

