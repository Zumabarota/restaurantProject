from django.db import models


class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('cup', 'Cup'),
        ('ea', '#'),
        ('g', 'grams'),
        ('ml', 'mL'),
    ]
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=10, default="", choices=UNIT_CHOICES)
    unit_price = models.DecimalField(max_digits=3, decimal_places=2)

    def get_absolute_url(self):
        return '/ingredient/list'

    def __str__(self):
        return f'{self.unit} {self.name}'
        # return f'{self.quantity} {self.name}, ${self.unit_price} each'


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def get_absolute_url(self):
        return '/menuitem/list'

    def __str__(self):
        return self.name
        # return f'{self.name}, ${self.price}'


class Purchase(models.Model):
    amount = models.IntegerField(default=1)
    # TODO: not sure how best to account for deleting MenuItems while retaining Purchases
    menuitem = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return '/purchase/list'

    def __str__(self):
        # return self.menuitem
        return f'{self.date}: {self.amount} {self.menuitem}'


# TODO: implement a way to have deleting an Ingredient flow through RecipeRequirement to delete the associated MenuItem
class RecipeRequirement(models.Model):
    amount = models.IntegerField(default=1)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    def __str__(self):
        # return self.menuitem
        return f'{self.amount} {self.ingredient} for {self.menuitem}'
