from django.shortcuts import get_object_or_404, redirect, render

from ..forms import BudgetForm
from ..models import Budget


def budget_list(request):
    budgets = Budget.objects.all()
    return render(request, "finance/budget_list.html", {"budgets": budgets})


def budget_create(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("finance:budget_list")
    else:
        form = BudgetForm()
    return render(request, "finance/budget_form.html", {"form": form})


def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect("finance:budget_list")
    else:
        form = BudgetForm(instance=budget)

    return render(request, "finance/budget_form.html", {"form": form})


def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == "POST":
        budget.delete()
        return redirect("finance:budget_list")

    return render(request, "finance/budget_confirm_delete.html", {"object": budget})
