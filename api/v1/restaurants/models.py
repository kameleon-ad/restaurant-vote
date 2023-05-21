from django.db import models


class Restaurants(models.Model):
    name = models.CharField(max_length=127, blank=False)
