from django import forms
from .models import Account, Category, Budget, Transaction, RecurringTransaction

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "account_type", "initial_balance", "color_hex", "active"] 



class CategoryForm(forms.ModelForm): 
    class Meta: 
        model = Category 
        fields = ["name", "category_type", "icon", "cor_hex", "parent_category"] 



class BudgetForm(forms.ModelForm): 
    class Meta: 
        model = Budget 
        fields = ["limit_value", "month_reference", "year_reference", "category"] 


class TransactionForm(forms.ModelForm): 
    class Meta: 
        model = Transaction 
        fields = ["description", "value", "transaction_date", "observation", "transaction_type", "transaction_status", "account", "destiny_account", "category"] 


class RecurringTransactionForm(forms.ModelForm): 
    class Meta: 
        model = RecurringTransaction 
        fields = ["description", "value", "recurring_type", "frequency", "due_date", "active", "account", "category"]