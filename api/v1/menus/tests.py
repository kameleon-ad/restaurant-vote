from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from datetime import date, timedelta
from api.v1.restaurants.models import Restaurants
from api.v1.menus.models import Menus, Votes
from api.v1.menus.views import MenusViewSetV1


class MenusModelAPITestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = MenusViewSetV1.as_view({'get': 'list', 'post': 'create'})

    def test_create_menu(self):
        # Create a test user
        user = User.objects.create_user(username='test_user', password='test_password')

        # Create a test restaurant
        restaurant = Restaurants.objects.create(name='Test Restaurant')

        # Create a test menu
        menu_data = {
            'restaurant': restaurant.id,
            'date': str(date.today()),
            'menu': 'Test Menu'
        }

        request = self.factory.post('/api/v1/menus/', data=menu_data)
        force_authenticate(request, user=user)
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Menus.objects.count(), 1)
        self.assertEqual(Menus.objects.first().menu, 'Test Menu')

    def test_get_menu_results(self):
        today = date.today()
        yesterday = today - timedelta(days=1)

        user1 = User.objects.create_user(username='test_user1', password='test_password1')
        user2 = User.objects.create_user(username='test_user2', password='test_password2')
        user3 = User.objects.create_user(username='test_user3', password='test_password3')
        # Create some test menus and votes
        restaurant = Restaurants.objects.create(name='Test Restaurant')
        menu1 = Menus.objects.create(restaurant=restaurant, date=today, menu='Menu 1')
        menu2 = Menus.objects.create(restaurant=restaurant, date=yesterday, menu='Menu 2')
        Votes.objects.create(employee=user1, menu=menu1, point=3)
        Votes.objects.create(employee=user2, menu=menu1, point=2)
        Votes.objects.create(employee=user3, menu=menu2, point=1)

        request = self.factory.get('/api/v1/menus/result/')
        force_authenticate(request, user=user1)
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['menu'], menu1.menu)
        self.assertEqual(response.data[1]['menu'], menu2.menu)
