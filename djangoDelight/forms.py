from django.forms import ModelForm, inlineformset_factory
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement


class IngredientCreateUpdateForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = {'name', 'unit', 'quantity', 'unit_price'}


class MenuItemCreateUpdateForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = {'name', 'price'}


class PurchaseCreateUpdateForm(ModelForm):
    class Meta:
        model = Purchase
        fields = {'amount', 'menuitem'}


class RecipeRequirementCreateForm(ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = {'amount', 'ingredient'}


RecipeRequirementFormSet = inlineformset_factory(
    MenuItem, RecipeRequirement, fields=['amount', 'ingredient'],
)
