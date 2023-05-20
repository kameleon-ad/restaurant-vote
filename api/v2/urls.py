# api/v2/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.v2.user.views import UserAPIView
from api.v2.auth.views import AuthAPIView
from api.v2.restaurant.views import RestaurantViewSet

router = DefaultRouter()
router.register('rest', RestaurantViewSet)

urlpatterns = [
    path('user/', UserAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('', include(router.urls)),
]
