from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from datetime import date
from api.v1.menus.views import MenusViewSetV1
from api.v1.menus.models import Menus, Votes
from api.v1.menus.serializers import VotesSerializer
from api.v2.menus.forms import VoteMenuFormV2


class MenusViewSetV2(MenusViewSetV1):
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
