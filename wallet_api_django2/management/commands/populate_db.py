import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from wallet_api_django2.models import Wallet, Transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados fictícios'

    def handle(self, *args, **kwargs):
        # Cria usuários
        users = []
        for i in range(1, 6):
            user = User.objects.create_user(
                cpf=f'1234567890{i}',
                full_name=f'Usuário {i}',
                password='senha123'
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Usuário {i} criado'))

        # Realiza depósitos
        for user in users:
            wallet = Wallet.objects.get(user=user)
            amount = Decimal(random.uniform(100, 1000))
            wallet.balance += amount
            wallet.save()
            Transaction.objects.create(
                receiver=user,
                amount=amount,
                transaction_type='DEPOSIT',
                status='SUCCESS'
            )

        # Realiza transferências
        for sender in users:
            for receiver in users:
                if sender != receiver:
                    amount = Decimal(random.uniform(10, 100))
                    if sender.wallet.balance >= amount:
                        sender.wallet.balance -= amount
                        receiver.wallet.balance += amount
                        sender.wallet.save()
                        receiver.wallet.save()
                        Transaction.objects.create(
                            sender=sender,
                            receiver=receiver,
                            amount=amount,
                            transaction_type='TRANSFER',
                            status='SUCCESS'
                        )
                    else:
                        Transaction.objects.create(
                            sender=sender,
                            receiver=receiver,
                            amount=amount,
                            transaction_type='TRANSFER',
                            status='FAILED'
                        )

        self.stdout.write(self.style.SUCCESS('Dados populados com sucesso!'))