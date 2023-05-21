# api/v1/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import include, path
from api.v1.employees.views import UserAPIView
from api.v1.auth.views import AuthAPIView
from api.v1.restaurants.views import RestaurantsViewSetV1
from api.v1.menus.views import MenusViewSetV1

router = DefaultRouter()
router.register('restaurants', RestaurantsViewSetV1)
router.register('menus', MenusViewSetV1)

urlpatterns = [
    path('employees/', UserAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('', include(router.urls)),
]
