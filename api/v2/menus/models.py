from django.db import models
from api.v2.restaurants.models import Restaurants


class Menus(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateField(blank=False, null=False)
    menu = models.TextField(blank=False, null=False)

    class Meta:
        unique_together = ['restaurant', 'date']
