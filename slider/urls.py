from django.conf.urls import url

from slider import views

urlpatterns = [
    url(r'^create_page/$', views.create_page, name='create_page'),
    url(r'^create/$', views.create, name='create'),
    url(r'^home/$', views.home, name='slider_home'),
    url(r'^$', views.home, name='slider_home'),
    url(r'^detail/(?P<slider_id>[0-9]+)/$', views.detail, name='slider_detail'),
    # TODO Right way?
    url(r'^detail/$', views.home, name='home'),
]
