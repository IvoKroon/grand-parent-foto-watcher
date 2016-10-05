from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('users.urls')),
    url(r'^images/', include('photo.urls')),
    url(r'^slider/', include('slider.urls')),
]
# for the images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
