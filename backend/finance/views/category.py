from django.shortcuts import get_object_or_404, redirect, render

from ..forms import CategoryForm
from ..models.category import Category


def category_list(request):
    categories = Category.objects.all()
    return render(request, "finance/category_list.html", {"categories": categories})


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("finance:category_list")
    else:
        form = CategoryForm()
    return render(request, "finance/category_form.html", {"form": form})


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("finance:category_list")
    else:
        form = CategoryForm(instance=category)

    return render(request, "finance/category_form.html", {"form": form})


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("finance:category_list")

    return render(request, "finance/category_confirm_delete.html", {"object": category})
