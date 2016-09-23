from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^detail/$', views.detail, name='detail'),
    url(r'^create/$', views.create, name='create'),
    url(r'^success/$', views.success, name='success'),
]
