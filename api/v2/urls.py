# api/v2/urls.py

from django.urls import path
from api.v2.user.views import UserAPIView
from api.v2.auth.views import AuthAPIView

urlpatterns = [
    path('user/', UserAPIView.as_view()),
    path('auth/', AuthAPIView.as_view()),
]
