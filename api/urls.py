# api/urls.py

from django.urls import include, path, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Lunch Voting API",
      default_version='v2',
      description="Documents for the Lunch Voting API (version 2)",
      contact=openapi.Contact(email="grib.platon@outlook.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('v1/', include('api.v1.urls')),
    path('v2/', include('api.v2.urls')),
]
