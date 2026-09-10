from django.contrib import admin

from .models import Account, Budget, Category, RecurringTransaction, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type", "initial_balance", "active")
    list_filter = ("account_type", "active")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_type", "parent_category")
    list_filter = ("category_type",)
    search_fields = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "value",
        "transaction_type",
        "transaction_status",
        "account",
        "destiny_account",
        "category",
        "transaction_date",
    )
    list_filter = ("transaction_type", "transaction_status", "account")
    search_fields = ("description",)
    date_hierarchy = "transaction_date"


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("category", "month_reference", "year_reference", "limit_value")
    list_filter = ("year_reference", "month_reference", "category")


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "value",
        "recurring_type",
        "frequency",
        "due_date",
        "account",
        "category",
        "active",
    )
    list_filter = ("recurring_type", "frequency", "active")
    search_fields = ("description",)
