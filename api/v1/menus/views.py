from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import F, Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: MenusSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def today(self, request: Request):
        menus_today = Menus.objects.filter(date=date.today())
        serializer = MenusSerializer(menus_today, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'menu_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['menu_id'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Vote successful",
                schema=VotesSerializer(),
                examples={
                    "application/json": {
                        {
                            "employee": "user2",
                            "failed": 2,
                            "succeed": 1,
                            "result": [
                                {
                                    "id": 56,
                                    "point": 2,
                                    "employee": 3,
                                    "menu": 4
                                }
                            ]
                        }
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid request or data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Menu not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
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

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))},
    )
    @action(detail=False, methods=['get'])
    def result(self, request: Request):
        results = Votes.objects.filter(menu__date=date.today()) \
            .values('menu', menu_des=F('menu__menu'), restaurant=F('menu__restaurant__name')) \
            .annotate(total_points=Sum('point')).order_by('-total_points')
        return Response(results)
