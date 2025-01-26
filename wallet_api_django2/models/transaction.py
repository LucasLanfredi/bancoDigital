from django.db import models
from .user import User

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Depósito'
        TRANSFER = 'TRANSFER', 'Transferência'

    class StatusType(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Sucesso'
        FAILED = 'FAILED', 'Falha'

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_transactions'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_transactions'
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices
    )
    status = models.CharField(
        max_length=20,
        choices=StatusType.choices
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.get_transaction_type_display()} - {self.amount}'