from django.urls import include, path
from rest_framework.routers import DefaultRouter
# drf-yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

from .views import ProfileViewSet

API_VERSION = 'v1'

router_v1 = DefaultRouter()

router_v1.register('users', ProfileViewSet, basename='profile')
urlpatterns = [
    # our api endpoints
    path('', include(router_v1.urls)),
]

# schema settings for drf yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Radioclub-API",
        default_version=API_VERSION,
        description="Self generating API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=settings.EMAIL_HOST_USER),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# drf-yasg urls
# self-generating API
urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

urlpatterns = [path(f'{API_VERSION}/', include(urlpatterns))]
