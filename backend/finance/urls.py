from django.urls import path

from .views import account, budget, category

app_name = "finance"

urlpatterns = [
    path("accounts/", account.account_list, name="account_list"),
    path("accounts/new/", account.account_create, name="account_create"),
    path("accounts/<int:pk>/edit/", account.account_upgrade, name="account_update"),
    path("accounts/<int:pk>/delete/", account.account_delete, name="account_delete"),
    path("categories/", category.category_list, name="category_list"),
    path("categories/new/", category.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", category.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", category.category_delete, name="category_delete"),
    path("budgets/", budget.budget_list, name="budget_list"),
    path("budgets/new/", budget.budget_create, name="budget_create"),
    path("budgets/<int:pk>/edit/", budget.budget_update, name="budget_update"),
    path("budgets/<int:pk>/delete/", budget.budget_delete, name="budget_delete"),
]
