from django.contrib import admin
from djangoDelight.models import Ingredient, MenuItem, Purchase, RecipeRequirement
# Register your models here.
admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(Purchase)
admin.site.register(RecipeRequirement)