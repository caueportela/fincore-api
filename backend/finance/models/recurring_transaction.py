from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .base import BaseModel


class RecurringTransaction(BaseModel):
    class RecurringType(models.TextChoices):
        INCOME = ("income"), ("receitas")
        EXPENSES = ("expenses"), ("despesas")

    class Frequency(models.TextChoices):
        MONTHLY = ("monthly"), ("mensal")
        WEEKLY = ("weekly"), ("semanal")
        ANNUAL = ("annual"), ("anual")

    description = models.CharField("Descrição", max_length=200)
    value = models.DecimalField("Valor", max_digits=12, decimal_places=2)
    recurring_type = models.CharField(
        "Tipo de Transação",
        max_length=20,
        choices=RecurringType.choices,
    )
    frequency = models.CharField(
        "Frequência",
        max_length=20,
        choices=Frequency.choices,
        default=Frequency.MONTHLY,
    )
    due_date = models.IntegerField(
        "Dia de Vencimento",
        validators=[MinValueValidator(1), MaxValueValidator(31)],
    )
    active = models.BooleanField("Ativa", default=True)

    account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE,
        related_name="recorrencias",
        verbose_name="Conta",
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorrencias",
        verbose_name="Categoria",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Transação Recorrente"
        verbose_name_plural = "Transações Recorrentes"
        ordering = ["-created_at"]
        db_table = "finance_recurring_transaction"
        indexes = [
            models.Index(fields=["created_at"], name="recurring_created_idx"),
            models.Index(fields=["updated_at"], name="recurring_updated_idx"),
            models.Index(fields=["deleted_at"], name="recurring_deleted_idx"),
        ]

    def __str__(self):
        return f"{self.description} - R$ {self.value}"

    def clean(self):
        super().clean()
        if self.due_date is not None and not (1 <= self.due_date <= 31):
            raise ValidationError(
                {"due_date": "O dia de vencimento deve estar entre 1 e 31."}
            )
