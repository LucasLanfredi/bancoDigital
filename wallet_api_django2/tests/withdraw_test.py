from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User, Wallet, Transaction

class WithdrawTests(APITestCase):
    def setUp(self):
        # Cria o usuário (o signal cria o Wallet automaticamente)
        self.user = User.objects.create_user(
            cpf='12345678901',
            full_name='Fulano de Tal',
            password='SenhaSegura123'
        )

        # Obtém o token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Configura o cabeçalho de autenticação
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Faz um depósito inicial de 1000 via endpoint
        deposit_url = reverse('deposit')
        response = self.client.post(
            deposit_url,
            {'amount': 1000.00},
            format='json'
        )

        self.wallet = self.user.wallet
        self.wallet.refresh_from_db()

    def test_withdraw_success(self):
        url = reverse('withdraw')
        data = {'amount': 500.00}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.wallet.refresh_from_db()

        self.assertEqual(self.wallet.balance, 500.00)

        transaction = Transaction.objects.first()
        self.assertEqual(transaction.amount, 500.00)
        self.assertEqual(transaction.transaction_type, 'WITHDRAW')
        self.assertEqual(transaction.status, 'SUCCESS')

    def test_withdraw_insufficient_balance(self):
        url = reverse('withdraw')
        data = {'amount': 1500.00}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Saldo insuficiente", response.data['error'])