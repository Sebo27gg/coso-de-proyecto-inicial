from django.db import models
from django.contrib.auth.models import User

class allergy(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User, blank=True)

class ingredient(models.Model):
    name = models.CharField(max_length=100)
    allergies = models.ManyToManyField(allergy, blank=True)

class product(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(ingredient, blank=True)

