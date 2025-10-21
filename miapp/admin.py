from django.contrib import admin
from .models import Allergy, Ingredient, Product

# Register your models here.

admin.site.register(Allergy) 
admin.site.register(Ingredient)
admin.site.register(Product)
