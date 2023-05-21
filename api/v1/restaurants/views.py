from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Restaurants
from .serializers import RestaurantsSerializer


class RestaurantsViewSetV1(ModelViewSet):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]
