from django import forms
from .models import Account, Category

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "account_type", "initial_balance", "color_hex", "active"] 



class CategoryForm(forms.ModelForm): 
    class Meta: 
        model = Category 
        fields = ["name", "category_type", "icon", "cor_hex", "parent_category"]