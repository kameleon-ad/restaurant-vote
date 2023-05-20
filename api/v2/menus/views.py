from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from datetime import date
from .models import Menus
from .serializers import MenusSerializer


class MenusViewSet(ModelViewSet):
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request: Request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant')
        req_date = request.data.get('date')
        menu_exists = Menus.objects.filter(restaurant=restaurant_id, date=req_date).exists()
        if menu_exists:
            menu = Menus.objects.get(restaurant=restaurant_id, date=req_date)
            serializer = self.get_serializer(menu, data=request.data)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def today(self, request: Request):
        menus_today = Menus.objects.filter(date=date.today())
        serializer = MenusSerializer(menus_today, many=True)
        return Response(serializer.data)
