from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('authentication.urls', namespace='authentication')),
]

from django.conf.urls import include, url
from django.contrib import admin
#serve media file in dev env
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

   
    url(r'^api/', include('authentication.urls', namespace='authentication')),
    url(r'^api/', include('profile.urls', namespace='profile')),
]