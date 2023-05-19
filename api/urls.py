# api/urls.py

from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('v1/', include('api.v1.urls')),
    path('v2/', include('api.v2.urls')),
]