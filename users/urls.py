from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^error/$', views.error, name='error'),
    url(r'^user/create_user/$', views.create_user, name='create_user'),
]
