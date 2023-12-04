from django.db import models
from django.contrib.auth.models import User, AbstractUser


class TravelItem(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class TravelPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 300)
    destination = models.CharField(max_length=300)
    travel_datetime = models.DateTimeField()
    travel_items = models.ManyToManyField(TravelItem)

    def __str__(self):
        return self.title

