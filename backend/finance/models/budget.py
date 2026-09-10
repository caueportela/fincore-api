from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .base import BaseModel


class Budget(BaseModel):  
    limit_value = models.DecimalField(max_digits=12, decimal_places=2) 
    month_reference = models.IntegerField( 
        validators=[ 
            MinValueValidator(1), 
            MaxValueValidator(12), 
        ]
    )
    year_reference = models.IntegerField(
        "Ano de Referência",
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )

    category = models.ForeignKey(
             "Category",
             on_delete=models.CASCADE, 
             verbose_name="Categoria",
             related_name="budgets",
         )   
    class Meta(BaseModel.Meta):
        verbose_name = "Orçamento Mensal"
        verbose_name_plural = "Orçamentos Mensais"
        ordering = ["-year_reference", "-month_reference"]
        db_table = "finance_budget" 

    #Garante que não existam 2 orçamentos ativos para a mesma categoria no mesmo mês/ano
        constraints = [
            models.UniqueConstraint(
                fields=["category", "month_reference", "year_reference"],
                condition=models.Q(deleted_at__isnull=True),
                name="unique_active_budget_per_category_period",
            )
        ]

    def __str__(self):
        return f"{self.category} - {self.month_reference}/{self.year_reference}: R$ {self.limit_value}"