from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),  # core api

] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)  # for imgs and files

if settings.DEBUG:
    # if project is in debug mode add debug toolbar
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')),)
