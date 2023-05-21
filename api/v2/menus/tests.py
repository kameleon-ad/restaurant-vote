import json

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from api.v2.menus.views import MenusViewSetV2
from api.v1.menus.serializers import VotesSerializer


class MenusViewSetV2TestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = MenusViewSetV2.as_view({'post': 'vote'})
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_vote_with_valid_data(self):
        # Create a POST request with valid data
        data = {'votes': "[1, 2, 3]"}
        request = self.factory.post('/api/v2/menus/vote/', data=data)

        # Set the user on the request for authentication
        force_authenticate(request, user=self.user)

        # Make the request
        response = self.view(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vote_with_invalid_data(self):
        # Create a POST request with invalid data
        data = {'votes': 'invalid'}
        request = self.factory.post('/menus/vote/', data=data)

        # Set the user on the request for authentication
        force_authenticate(request, user=self.user)

        # Make the request
        response = self.view(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert the response data
        expected_data = {'message': 'Vote form must be non-empty json.'}
        self.assertEqual(response.data, expected_data)

    def test_vote_with_exceeding_votes_limit(self):
        # Create a POST request with exceeding votes limit
        data = {'votes': "[1, 2, 3, 4]"}
        request = self.factory.post('/api/v2/menus/vote/', data=data)

        # Set the user on the request for authentication
        force_authenticate(request, user=self.user)

        # Make the request
        response = self.view(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert the response data
        expected_data = {'message': 'Only three votes allowed'}
        self.assertEqual(response.data, expected_data)

    def test_vote_with_invalid_menu_id(self):
        # Create a POST request with invalid menu IDs
        data = {'votes': "[10, 20, 30]"}
        request = self.factory.post('/menus/vote/', data=data)

        # Set the user on the request for authentication
        force_authenticate(request, user=self.user)

        # Make the request
        response = self.view(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data
        expected_data = {
            'employee': self.user.username,
            'failed': 3,
            'succeed': 0,
            'result': VotesSerializer(instance=[], many=True).data
        }
        self.assertEqual(response.data, expected_data)

    def test_vote_without_authentication(self):
        # Create a POST request without authentication
        data = {'votes': "[1, 2, 3]"}
        request = self.factory.post('/menus/vote/', data=data)

        # Make the request without authenticating the user

        # Make the request
        response = self.view(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
