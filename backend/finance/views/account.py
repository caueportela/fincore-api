from django.shortcuts import get_object_or_404, redirect, render

from ..forms import AccountForm
from ..models.account import Account


def account_list(request):
    accounts = Account.objects.all()
    return render(request, "finance/account_list.html", {"accounts": accounts})


def account_create(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("finance:account_list")
    else:
        form = AccountForm()
    return render(request, "finance/account_form.html", {"form": form})


def account_upgrade(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect("finance:account_list")
    else:
        form = AccountForm(instance=account)

    return render(request, "finance/account_form.html", {"form": form})


def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == "POST":
        account.delete()
        return redirect("finance:account_list")

    return render(request, "finance/account_confirm_delete.html", {"object": account})
