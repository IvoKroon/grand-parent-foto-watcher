from django.shortcuts import render


def custom_404(request):
    return render(request, "404/index.html")


def custom_403(request):
    return render(request, "404/index.html")


def custom_400(request):
    return render(request, "404/index.html")


def custom_500(request):
    return render(request, "404/index.html")
