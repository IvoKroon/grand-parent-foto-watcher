from django.conf.urls import url

from slider import views

urlpatterns = [
    url(r'^create_page/$', views.create_page, name='create_page'),
    url(r'^create/$', views.create, name='create'),
    url(r'^home/$', views.home, name='slider_home'),
    url(r'^$', views.home, name='slider_home'),
    url(r'^detail/(?P<slider_id>[0-9]+)/$', views.detail, name='slider_detail'),
    # TODO Right way? To let user go to home when no id is selected
    url(r'^detail/$', views.home, name='home'),

    url(r'^image/(?P<slider_id>[0-9]+)/$', views.add_image_to_slider, name='add_image_to_slider'),
    url(r'^image/add/(?P<slider_id>[0-9]+)/$', views.add_image, name='add_image'),

    url(r'^ajax/remove/(?P<slider_id>[0-9]+)/(?P<image_id>[0-9]+)$', views.remove_image_from_slider, name='remove_image_from_slider'),
    url(r'^ajax/change_slider_status/$', views.switch_slider_status, name='switch slider status'),
]
