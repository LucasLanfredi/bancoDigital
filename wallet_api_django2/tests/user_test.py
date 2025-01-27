from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User


class AuthenticationTests(APITestCase):
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

    # Testes de Registro
    def test_user_registration_success(self):
        url = reverse('register')
        data = {
            'cpf': '98765432109',
            'full_name': 'Beltrano Silva',
            'password': 'OutraSenha456',
            'email': '98765432109@teste.com',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_registration_duplicate_cpf(self):
        url = reverse('register')
        data = {**self.user_data}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cpf', response.data)

    def test_login_success(self):
        url = reverse('login')
        data = {
            'cpf': self.user_data['cpf'],
            'password': self.user_data['password']
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        url = reverse('login')
        data = {
            'cpf': self.user_data['cpf'],
            'password': 'senha_errada'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid_cpf(self):
        url = reverse('login')
        data = {
            'cpf': '00000000000',
            'password': 'qualquer'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)