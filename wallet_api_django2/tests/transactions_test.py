from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User, Transaction


class TransactionTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            cpf='12345678901',
            full_name='Fulano de Tal',
            password='senha123'
        )
        self.user2 = User.objects.create_user(
            cpf='98765432109',
            full_name='Beltrano Silva',
            password='senha456'
        )

        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        deposit_url = reverse('deposit')
        self.client.post(deposit_url, {'amount': 1000.00}, format='json')

    def test_deposit_transaction_creation(self):
        """
        Verifica se um depósito cria uma transação corretamente.
        """
        transactions = Transaction.objects.filter(transaction_type='DEPOSIT')
        self.assertEqual(transactions.count(), 1)

        deposit = transactions.first()
        self.assertEqual(deposit.receiver, self.user1)
        self.assertEqual(deposit.amount, 1000.00)
        self.assertEqual(deposit.status, 'SUCCESS')

    def test_withdraw_transaction_creation(self):
        """
        Verifica se um saque cria uma transação corretamente.
        """
        # Faz um saque
        withdraw_url = reverse('withdraw')
        self.client.post(withdraw_url, {'amount': 500.00}, format='json')

        transactions = Transaction.objects.filter(transaction_type='WITHDRAW')
        self.assertEqual(transactions.count(), 1)

        withdraw = transactions.first()
        self.assertEqual(withdraw.sender, self.user1)
        self.assertEqual(withdraw.amount, 500.00)
        self.assertEqual(withdraw.status, 'SUCCESS')

    def test_transfer_transaction_creation(self):
        """
        Verifica se uma transferência cria uma transação corretamente.
        """
        transfer_url = reverse('transfer')
        data = {
            'receiver_cpf': '98765432109',
            'amount': 300.00
        }

        response = self.client.post(transfer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        transactions = Transaction.objects.filter(transaction_type='TRANSFER')
        self.assertEqual(transactions.count(), 1)

        transfer = transactions.first()
        self.assertEqual(transfer.sender, self.user1)
        self.assertEqual(transfer.receiver, self.user2)
        self.assertEqual(transfer.amount, 300.00)
        self.assertEqual(transfer.status, 'SUCCESS')

    def test_insufficient_balance_transfer(self):
        """
        Verifica se uma transferência sem saldo falha corretamente.
        """
        transfer_url = reverse('transfer')
        data = {
            'receiver_cpf': '98765432109',
            'amount': 1500.00  # Valor maior que o saldo
        }

        response = self.client.post(transfer_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        transactions = Transaction.objects.filter(transaction_type='TRANSFER', status='FAILED')
        self.assertEqual(transactions.count(), 1)

    def test_transaction_list_filtering(self):
        """
        Verifica o filtro de transações por período.
        """
        # Cria uma transação antiga
        old_transaction = Transaction.objects.create(
            sender=None,
            receiver=self.user1,
            amount=500.00,
            transaction_type='DEPOSIT',
            status='SUCCESS',
            timestamp=datetime.now() - timedelta(days=10)
        )

        # Obtém transações dos últimos 2 dias
        today = datetime.now().strftime('%Y-%m-%d')
        two_days_ago = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

        list_url = reverse('transaction-list') + f'?start_date={two_days_ago}&end_date={today}'
        response = self.client.get(list_url)

        # Apenas o depósito inicial (feito no setUp) deve aparecer
        self.assertEqual(len(response.data['transactions']), 1)
        self.assertEqual(response.data['transactions'][0]['amount'], '1000.00')