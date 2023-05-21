# api/v2/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.v1.employees.views import UserAPIView
from api.v1.auth.views import AuthAPIView
from api.v1.restaurants.views import RestaurantsViewSetV1
from api.v2.menus.views import MenusViewSetV2

router = DefaultRouter()
router.register('restaurants', RestaurantsViewSetV1)
router.register('menus', MenusViewSetV2)

urlpatterns = [
    path('employees/', UserAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
    path('', include(router.urls)),
]
