from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Account

ACCOUNT_FIELDS = ["name", "account_type", "initial_balance", "color_hex", "active"]


class AccountListView(ListView):
    model = Account
    template_name = "finance/account_list.html"
    context_object_name = "accounts"


class AccountCreateView(CreateView):
    model = Account
    fields = ACCOUNT_FIELDS
    template_name = "finance/account_form.html"
    success_url = reverse_lazy("finance:account_list")


class AccountUpdateView(UpdateView):
    model = Account
    fields = ACCOUNT_FIELDS
    template_name = "finance/account_form.html"
    success_url = reverse_lazy("finance:account_list")


class AccountDeleteView(DeleteView):
    model = Account
    template_name = "finance/account_confirm_delete.html"
    success_url = reverse_lazy("finance:account_list")
