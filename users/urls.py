from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^success/$', views.success, name='thanks'),
    url(r'^success/(?P<success_id>[0-9]+)/$', views.success, name='thanks'),
    # url(r'^project_config/$', views.foo),
    # url(r'^project_config/(?P<product>\w+)/$', views.foo),
    url(r'^error/$', views.error, name='error'),
    url(r'^user/create_user/$', views.create_user, name='create_user'),
    url(r'^user/check_user/$', views.check_user, name='check_user'),
    url(r'^home/$', views.home, name='create'),

    url(r'^user/logout/$', views.logout, name='logout'),

    url(r'^user/profile/$', views.profile, name='profile'),
    url(r'^user/profile_update/$', views.edit_user, name='profile_update'),
]
