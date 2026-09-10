from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel


class Account(BaseModel):
    class AccountType(models.TextChoices):
        BANK = "bank", ("Conta Bancaria")
        WALLET = "wallet", ("Carteira")
        CREDIT_CARD = "credit_card", ("Cartão de Crédito")
        INVESTMENT = "investment", ("Investimento")

    name = models.CharField("Nome", max_length=100)
    account_type = models.CharField(
        "Tipo de Conta",
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.BANK,
    )
    initial_balance = models.DecimalField(
        "Saldo Inicial",
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )
    color_hex = models.CharField("Cor", max_length=7, default="#319795")
    active = models.BooleanField("Ativa", default=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Conta Financeira" 
        verbose_name_plural = "Contas Financeiras"
        ordering =["-created_at"] 
        db_table = "finance_account" 

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.account_type == self.AccountType.WALLET and self.initial_balance is not None and self.initial_balance < 0:
            raise ValidationError(
                {"initial_balance": "Contas do tipo Carteira não podem ter saldo inicial negativo."}
            )