from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User, Transaction


class DepositTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'cpf': '12345678901',
            'full_name': 'Fulano de Tal',
            'password': 'SenhaSegura123',
            'email': '12345678901@teste.com'
        }

        self.user = User.objects.create_user(
            cpf=self.user_data['cpf'],
            full_name=self.user_data['full_name'],
            password=self.user_data['password']
        )

        self.wallet = self.user.wallet

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_deposit_success(self):
        url = reverse('deposit')
        data = {'amount': 1000.00}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, 1000.00)

        transaction = Transaction.objects.first()
        self.assertEqual(transaction.amount, 1000.00)
        self.assertEqual(transaction.transaction_type, 'DEPOSIT')
        self.assertEqual(transaction.status, 'SUCCESS')

    def test_deposit_negative_amount(self):
        url = reverse('deposit')
        data = {'amount': -100.00}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)