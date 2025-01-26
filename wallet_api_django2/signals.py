from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Wallet

# signals.py
@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    """
    Cria uma Wallet automaticamente quando um User é criado.
    """
    if created:
        Wallet.objects.create(user=instance, balance=0.00)