from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os

# Funcion path_and_rename: Sirve unica y exclusivamente para que las imagenes de los productos se guarden
# automaticamente con su nombre en media/products
def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(instance.slug, ext)
        return os.path.join(path, filename)
    return wrapper

# Modelo de Ingredientes
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    # Para evitar ingredientes repetidos, el formato de los ingredientes siempre debe ser:
    # Primera letra en mayuscula, el resto en minuscula
    def clean(self):
        self.name = self.name[0].upper() + self.name[1:].lower()
        for ingredient in Ingredient.objects.all():
            if ingredient.name == self.name:
                raise ValidationError("Esta usted creando un ingrediente ya existente")
    
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
    
    # Para evitar Alergias repetidos, repetimos el mismo metodo que con los ingredientes
    def clean(self):
        self.name = self.name[0].upper() + self.name[1:].lower()
        for allergy in Allergy.objects.all():
            if allergy.name == self.name and allergy != self:
                raise ValidationError("Esta usted creando una alergia ya existente")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# Modelo de Producto 
class Product(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, blank=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    photo = models.ImageField(upload_to=path_and_rename('products/'))
    favorite_of = models.ManyToManyField(User, blank=True)

    class Meta: 
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    # Funcionalidades extra para que añadir nuevos productos sea mas facil:
    # el slug se crea solo al guardar y la imagen se borra sola al eliminar
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
        return super().delete(*args, **kwargs)
    
        