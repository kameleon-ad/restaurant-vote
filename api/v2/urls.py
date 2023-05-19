# api/v2/urls.py

from django.urls import path
from api.v2.user.views import UserAPIView

urlpatterns = [
    path('user/', UserAPIView.as_view())
]
