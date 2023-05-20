# api/v2/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.v2.employees.views import UserAPIView
from api.v2.auth.views import AuthAPIView
from api.v2.restaurants.views import RestaurantsViewSet

router = DefaultRouter()
router.register('rest', RestaurantsViewSet)

urlpatterns = [
    path('employees/', UserAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('', include(router.urls)),
]
