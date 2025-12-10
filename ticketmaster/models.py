from django.contrib.auth.models import User
from django.db import models

class Favorite(models.Model):
    tm_id = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=255)
    venue = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    event_date = models.CharField(max_length=100, blank=True)
    event_time = models.CharField(max_length=50, blank=True)
    url = models.URLField(max_length=500, blank=True)
    image = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city})"
