from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Allergy(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    users = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return self.name