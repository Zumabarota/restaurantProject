from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientCreateUpdateForm, MenuItemCreateUpdateForm, PurchaseCreateUpdateForm,\
    RecipeRequirementFormSet


@login_required
def home(request):
    context = {"name": request.user}
    return render(request, 'djangoDelight/home.html', context)


class IngredientList(LoginRequiredMixin, ListView):
    model = Ingredient


class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = 'djangoDelight/ingredient_createupdate_form.html'
    form_class = IngredientCreateUpdateForm


class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = 'djangoDelight/ingredient_createupdate_form.html'
    form_class = IngredientCreateUpdateForm


class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'djangoDelight/ingredient_delete_form.html'
    success_url = '/ingredient/list'


class MenuItemList(LoginRequiredMixin, ListView):
    model = MenuItem


class MenuItemCreate(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = 'djangoDelight/menuitem_createupdate_form.html'
    form_class = MenuItemCreateUpdateForm


class MenuItemUpdate(LoginRequiredMixin, UpdateView):
    model = MenuItem
    template_name = 'djangoDelight/menuitem_createupdate_form.html'
    form_class = MenuItemCreateUpdateForm


class MenuItemDelete(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'djangoDelight/menuitem_delete_form.html'
    success_url = '/menuitem/list'


class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase


class PurchaseCreate(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = 'djangoDelight/purchase_createupdate_form.html'
    form_class = PurchaseCreateUpdateForm


class PurchaseUpdate(LoginRequiredMixin, UpdateView):
    model = Purchase
    template_name = 'djangoDelight/purchase_createupdate_form.html'
    form_class = PurchaseCreateUpdateForm


class PurchaseDelete(LoginRequiredMixin, DeleteView):
    model = Purchase
    template_name = 'djangoDelight/purchase_delete_form.html'
    success_url = '/purchase/list'


@login_required
def manage_requirements(request, menu_item_pk):
    menu_item = MenuItem.objects.get(pk=menu_item_pk)
    formset_class = RecipeRequirementFormSet
    if request.method == 'POST':
        formset = formset_class(request.POST, instance=menu_item)
        if formset.is_valid():
            formset.save()
            update_production_cost(menu_item)
            return redirect('menuitemlist')
    else:
        formset = formset_class(instance=menu_item)
        context = {
            'name': menu_item.name,
            'price': menu_item.price,
            'formset': formset,
            'menu_item_pk': menu_item_pk,
        }
        return render(request, 'djangoDelight/formset.html', context)


@login_required
def ingredient_update(request, ingredient_pk):
    ingredient = Ingredient.objects.get(pk=ingredient_pk)
    form = IngredientCreateUpdateForm(instance=ingredient)

    if request.method == 'POST':
        form = IngredientCreateUpdateForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            # Get all RecipeRequirement objects that involve the updated ingredient
            # for each, update the production cost of the associated MenuItem
            rr_objects = RecipeRequirement.objects.all().filter(ingredient=ingredient)
            for i in rr_objects:
                update_production_cost(i.menuitem)
            return redirect('ingredientlist')
    else:
        context = {
            'form': form,
            'ingredient_pk': ingredient_pk
        }
        return render(request, 'djangoDelight/ingredient_createupdate_form.html', context)


# (re)calculates the production cost of the specified MenuItem
def update_production_cost(menu_item):
    rr_objects = RecipeRequirement.objects.all().filter(menuitem=menu_item)
    production_cost = 0
    for i in rr_objects:
        production_cost += i.ingredient.unit_price * i.amount
    menu_item.cost = production_cost
    menu_item.save(update_fields=["cost"])


class ProfitReport(LoginRequiredMixin, ListView):
    def get(self, request):
        report = []
        dates = Purchase.objects.values('date').distinct()
        total_revenue = 0
        total_cost = 0
        for i in dates:
            menuitems = Purchase.objects.all().filter(date=i['date'])
            revenue = 0
            cost = 0
            for j in menuitems:
                revenue += j.menuitem.price * j.amount
                cost += j.menuitem.cost * j.amount
            total_revenue += revenue
            total_cost += cost
            report.append([i['date'], revenue, cost, revenue - cost])
        context = {
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'total_profit': total_revenue - total_cost,
            'report': report
        }
        return render(request, 'djangoDelight/profit_report.html', context)


def login_view(request):
    context = {
        "login_view": "active"
    }
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return HttpResponse("invalid credentials")
    return render(request, "djangoDelight/login.html", context)


def logout_view(request):
    # ... Other logic
    logout(request)
    return redirect("home")
