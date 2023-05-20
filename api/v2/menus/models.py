from django.db import models
from api.v2.restaurants.models import Restaurants
from django.contrib.auth.models import User


class Menus(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateField(blank=False, null=False)
    menu = models.TextField(blank=False, null=False)

    class Meta:
        unique_together = ['restaurant', 'date']


class Votes(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menus, on_delete=models.CASCADE)
    point = models.PositiveIntegerField(default=1)
