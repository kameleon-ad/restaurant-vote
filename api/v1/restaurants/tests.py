from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from api.v1.restaurants.views import RestaurantsViewSetV1
from api.v1.restaurants.models import Restaurants
from api.v1.restaurants.serializers import RestaurantsSerializer


class RestaurantsViewSetV1TestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = RestaurantsViewSetV1.as_view({'get': 'list', 'post': 'create'})
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_list_restaurants_authenticated(self):
        # Create some test restaurants
        Restaurants.objects.create(name='Restaurant A')
        Restaurants.objects.create(name='Restaurant B')

        # Create a GET request
        request = self.factory.get('/restaurants/')

        # Authenticate the request with the test user
        force_authenticate(request, user=self.user)

        # Make the request
        response = self.view(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data
        restaurants = Restaurants.objects.all()
        serializer = RestaurantsSerializer(restaurants, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_restaurant_admin(self):
        # Create a POST request with data
        data = {'name': 'New Restaurant'}
        request = self.factory.post('/restaurants/', data=data)

        # Set the user on the request as an admin
        request.user = self.user
        self.user.is_staff = True
        self.user.save()

        force_authenticate(request, user=self.user)

        # Make the request
        response = self.view(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert the created restaurant in the database
        restaurant = Restaurants.objects.get(name='New Restaurant')
        self.assertEqual(restaurant.name, 'New Restaurant')

    def test_create_restaurant_unauthorized(self):
        # Create a POST request with data
        data = {'name': 'New Restaurant'}
        request = self.factory.post('/restaurants/', data=data)

        # Make the request without authenticating the user

        # Make the request
        response = self.view(request)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
