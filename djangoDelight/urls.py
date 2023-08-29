from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("accounts/login/", auth_views.LoginView.as_view()),
    # path('accounts/', include("django.contrib.auth.urls"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('ingredient/list', views.IngredientList.as_view(), name="ingredientlist"),
    path('ingredient/create', views.IngredientCreate.as_view(), name="ingredientcreate"),
    # path('ingredient/update/<pk>', views.IngredientUpdate.as_view(), name="ingredientupdate"),
    path('ingredient/update/<int:ingredient_pk>', views.ingredient_update, name="ingredientupdate"),
    path('ingredient/delete/<int:pk>', views.IngredientDelete.as_view(), name="ingredientdelete"),
    path('menuitem/list', views.MenuItemList.as_view(), name="menuitemlist"),
    path('menuitem/create', views.MenuItemCreate.as_view(), name="menuitemcreate"),
    # path('menuitem/update/<pk>', views.MenuItemUpdate.as_view(), name="menuitemupdate"),
    path('menuitem/update/<int:menu_item_pk>', views.manage_requirements, name="formset"),
    path('menuitem/delete/<int:pk>', views.MenuItemDelete.as_view(), name="menuitemdelete"),
    path('purchase/list', views.PurchaseList.as_view(), name="purchaselist"),
    path('purchase/create', views.PurchaseCreate.as_view(), name="purchasecreate"),
    path('purchase/update/<int:pk>', views.PurchaseUpdate.as_view(), name="purchaseupdate"),
    path('purchase/delete/<int:pk>', views.PurchaseDelete.as_view(), name="purchasedelete"),
    path('report', views.ProfitReport.as_view(), name="profit_report")
]
