from django.db import models
from .user import User

class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Carteira'
        verbose_name_plural = 'Carteiras'

    def __str__(self):
        return f"Carteira do {self.user.full_name} (R$ {self.balance})"