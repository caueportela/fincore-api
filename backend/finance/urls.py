from django.urls import path

from .views import account

app_name = "finance"

urlpatterns = [
    path("accounts/", account.account_list, name="account_list"),
    path("accounts/new/", account.account_create, name="account_create"),
    path("accounts/<int:pk>/edit/", account.account_upgrade, name="account_update"),
    path("accounts/<int:pk>/delete/", account.account_delete, name="account_delete"),
]
