from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import static

handler400 = 'base.views.custom_400'
handler403 = 'base.views.custom_403'
handler404 = 'base.views.custom_404'
handler500 = 'base.views.custom_500'

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^', include('guest.urls')),
    url(r'^', include('users.urls')),

    url(r'^images/', include('photo.urls')),
    url(r'^slider/', include('slider.urls')),
    url(r'^search/', include('search.urls')),
]
# for the images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
