from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=127, blank=False)
