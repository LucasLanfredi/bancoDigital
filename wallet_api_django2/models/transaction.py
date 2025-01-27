from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Depósito'),
        ('WITHDRAW', 'Saque'),
        ('TRANSFER', 'Transferência'),
    )
    STATUS_CHOICES = (
        ('SUCCESS', 'Sucesso'),
        ('FAILED', 'Falha'),
    )

    sender = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_transactions'
    )
    receiver = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_transactions'
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"