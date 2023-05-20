from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Menus
from .serializers import MenusSerializer


class MenusViewSet(ModelViewSet):
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant')
        date = request.data.get('date')
        menu_exists = Menus.objects.filter(restaurant=restaurant_id, date=date).exists()
        if menu_exists:
            menu = Menus.objects.get(restaurant=restaurant_id, date=date)
            serializer = self.get_serializer(menu, data=request.data)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
