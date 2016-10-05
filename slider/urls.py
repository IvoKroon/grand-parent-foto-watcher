from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create_slider/$', views.create_slider, name='create_slider'),
]
