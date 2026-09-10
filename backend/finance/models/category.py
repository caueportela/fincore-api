from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel


class Category(BaseModel):  
    class CategoryType(models.TextChoices): 
        INCOME = ("income"), ("receitas") 
        EXPENSES = ("expenses"), ("despesas") 

    name = models.CharField("Nome", max_length=100)  
    category_type = models.CharField(                   
                "Tipo da Categoria", 
                max_length= 20, 
                choices = CategoryType.choices, 
                )
    icon = models.CharField("Icone", max_length=50, blank=True) 
    cor_hex = models.CharField("Cor da Categoria", max_length=7, default='#2B6CB0') 

    parent_category = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoria Pai",
        related_name="subcategories",
    )  


    class Meta(BaseModel.Meta): 
            verbose_name = "Categoria Financeira" 
            verbose_name_plural = "Categorias Financeiras"
            ordering =["-created_at"]
            db_table = "finance_category"
            indexes = [
                models.Index(fields=["created_at"], name="category_created_idx"),
                models.Index(fields=["updated_at"], name="category_updated_idx"),
                models.Index(fields=["deleted_at"], name="category_deleted_idx"),
            ]
    

    def __str__(self):
        return self.name

    # Validação obrigatória da especificação
    def clean(self):
        super().clean()
        if self.parent_category and self.parent_category.category_type != self.category_type:
            raise ValidationError(
                {"parent_category": "A subcategoria deve ter o mesmo tipo da categoria pai."}
            )