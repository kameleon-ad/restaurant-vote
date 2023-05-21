from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import date
from api.v1.menus.views import MenusViewSetV1
from api.v1.menus.models import Menus, Votes
from api.v1.menus.serializers import VotesSerializer
from api.v2.menus.forms import VoteMenuFormV2


class MenusViewSetV2(MenusViewSetV1):
    @swagger_auto_schema(
        method='post',
        operation_summary="Vote on menus",
        operation_description="Allows an employee to vote on menus for the current date.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'votes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                ),
            },
            required=['votes'],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Successful vote",
                schema=VotesSerializer(many=True),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid request or vote",
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
        form = VoteMenuFormV2(request.POST)

        if not form.is_valid():
            return Response({'message': 'Vote form must be non-empty json.'}, status=status.HTTP_400_BAD_REQUEST)

        votes = form.cleaned_data['votes']

        if not isinstance(votes, list):
            return Response({'message': 'Vote form must be list json.', 'type': votes}, status=status.HTTP_400_BAD_REQUEST)

        if len(votes) > 3:
            return Response({'message': 'Only three votes allowed'}, status=400)

        Votes.objects.filter(employee=employee.id, menu__date=date.today()).delete()

        failed, succeed = 0, 0
        votes_info = []
        for idx, menu_id in enumerate(votes):
            menu = Menus.objects.filter(id=menu_id, date=date.today()).first()
            if menu is None:
                failed += 1
                continue

            votes_info.append({
                'point': 3 - idx,
                'employee': employee.id,
                'menu': menu_id
            })
            succeed += 1

        serializer = VotesSerializer(data=votes_info, many=True)
        serializer.is_valid()
        serializer.save()

        return Response({'employee': employee.username, 'failed': failed, 'succeed': succeed, 'result': serializer.data})
