from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Transaction
from ..serializers import WalletSerializer, DepositSerializer, WithdrawSerializer


class BalanceView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet

class DepositView(generics.CreateAPIView):
    """
        Endpoint para depósito de valor na carteira
    """
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        wallet = self.request.user.wallet
        amount = serializer.validated_data['amount']

        with transaction.atomic():
            wallet.balance += amount
            wallet.save()

            Transaction.objects.create(
                receiver=self.request.user,
                amount=amount,
                transaction_type='DEPOSIT',
                status='SUCCESS'
            )

class WithdrawView(generics.CreateAPIView):
    """
        Endpoint para Saque de valor na carteira
    """
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            try:
                self.perform_create(serializer)
                return Response(
                    {"detail": "Saque realizado com sucesso."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

    def perform_create(self, serializer):
        wallet = self.request.user.wallet
        amount = serializer.validated_data['amount']

        with transaction.atomic():
            if wallet.balance < amount:
                raise ValueError("Saldo insuficiente para realizar o saque.")

            wallet.balance -= amount
            wallet.save()

            Transaction.objects.create(
                sender=self.request.user,
                receiver=None,
                amount=amount,
                transaction_type='WITHDRAW',
                status='SUCCESS'
            )