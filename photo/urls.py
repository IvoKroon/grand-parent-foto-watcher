from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.photo_home, name='photo_home'),
    url(r'^upload/$', views.photo_page, name='photo_page'),
    url(r'^uploading/$', views.image_uploading, name='image_uploading'),

]
