from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^images/$', views.photo_page, name='photo_page'),
    url(r'^image/upload/$', views.image_upload, name='image_upload'),

]
