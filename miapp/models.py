from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Allergy(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, blank=True)
    ingredients = models.ManyToManyField(Ingredient, blank=False)
    

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, blank=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    class Meta: 
        ordering = ["name"]
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
        