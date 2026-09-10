from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel


class Transaction(BaseModel):
    class TransactionType(models.TextChoices):
        INCOME = ("income"), ("receitas")
        EXPENSES = ("expenses"), ("despesas")
        TRANSFERENCE = ("transference"), ("transferência")

    class TransactionStatus(models.TextChoices):
        PENDING = ("pending"), ("pendente")
        COMPLETED = ("completed"), ("Completada")
        CANCELED = ("canceled"), ("cancelada")

    description = models.CharField("Descrição", max_length=200)
    value = models.DecimalField("Valor", max_digits=12, decimal_places=2)
    transaction_date = models.DateField("Data da Transação")
    observation = models.TextField("Observação", blank=True)

    transaction_type = models.CharField(
        "Tipo de Transação",
        max_length=20,
        choices=TransactionType.choices,
    )

    transaction_status = models.CharField(
        "Status da Transação",
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.COMPLETED,
    )
    account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Conta",
    )

    destiny_account = models.ForeignKey(
        "Account",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transferencias_recebidas",
        verbose_name="Conta Destino",
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="transactions",
        verbose_name="Categoria",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ["-transaction_date"]
        db_table = "finance_transaction" 
        indexes = [
            models.Index(fields=["created_at"], name="transaction_created_idx"),
            models.Index(fields=["updated_at"], name="transaction_updated_idx"),
            models.Index(fields=["deleted_at"], name="transaction_deleted_idx"),
            models.Index(fields=["transaction_date"], name="transaction_date_idx"),
        ]

    def __str__(self):
        return f"{self.description} - R$ {self.value}"

    def clean(self):
        super().clean()
        if self.value is not None and self.value <= 0:
            raise ValidationError({"value": "O valor deve ser maior que zero."})

        if self.transaction_type == self.TransactionType.TRANSFERENCE:
            if not self.destiny_account:
                raise ValidationError(
                    {"destiny_account": "Conta destino é obrigatória em transferências."}
                )
            if self.account_id and self.destiny_account_id == self.account_id:
                raise ValidationError(
                    {"destiny_account": "A conta destino não pode ser igual à conta de origem."}
                )
