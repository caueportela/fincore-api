from django.urls import path

from . import views

app_name = "finance"

urlpatterns = [
    path("accounts/", views.AccountListView.as_view(), name="account_list"),
    path("accounts/new/", views.AccountCreateView.as_view(), name="account_create"),
    path("accounts/<int:pk>/edit/", views.AccountUpdateView.as_view(), name="account_update"),
    path("accounts/<int:pk>/delete/", views.AccountDeleteView.as_view(), name="account_delete"),
]
