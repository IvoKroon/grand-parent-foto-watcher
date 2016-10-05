from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('users.urls')),
    url(r'^', include('photo.urls')),
    url(r'^', include('slider.urls')),
]
