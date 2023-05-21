from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import F, Sum
from datetime import date
from .models import Menus, Votes
from .serializers import MenusSerializer, VotesSerializer
from .forms import VoteMenuFormV1


class MenusViewSetV1(ModelViewSet):
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

    @action(detail=False, methods=['post'])
    def vote(self, request: Request):
        employee = request.user
        form = VoteMenuFormV1(request.POST)

        if not form.is_valid():
            return Response({'message': 'Vote form must have integer menu_id'}, status=status.HTTP_400_BAD_REQUEST)

        menu_id = form.cleaned_data.get('menu_id')
        menu = Menus.objects.filter(id=menu_id, date=date.today()).first()

        if menu is None:
            return Response({'message': 'Menu does not exist in today\' menu.'}, status=status.HTTP_404_NOT_FOUND)

        Votes.objects.filter(employee=employee.id, menu__date=date.today()).delete()
        serializer = VotesSerializer(data={
            'point': 1,
            'employee': employee.id,
            'menu': menu_id
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'employee': employee.username, 'result': serializer.data})

    @action(detail=False, methods=['get'])
    def result(self, request: Request):
        results = Votes.objects.filter(menu__date=date.today()) \
            .values('menu', menu_des=F('menu__menu'), restaurant=F('menu__restaurant__name')) \
            .annotate(total_points=Sum('point')).order_by('-total_points')
        return Response(results)
