from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from news.views import weather_view  # your weather_view import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', weather_view, name='weather'),  # <<< added here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
