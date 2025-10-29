from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Modelo de Ingredientes
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

    # Para evitar ingredientes repetidos, el formato de los ingredientes siempre debe ser:
    # Primera letra en mayuscula, el resto en minuscula
    def clean(self):
        cannon_name = self.name[0].upper()+ self.name[1:].lower()
        for ingredient in Ingredient.objects.all():
            if ingredient.name == cannon_name:
                raise ValidationError("Este ingrediente ya existe")
        self.name = cannon_name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# Modelo de alergias
class Allergy(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, blank=True)
    ingredients = models.ManyToManyField(Ingredient, blank=False)
    

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

# Modelo de Producto 
class Product(models.Model):

    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, blank=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    photo = models.ImageField(upload_to='')
    favorite_of = models.ManyToManyField(User, blank=True)

    class Meta: 
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
        