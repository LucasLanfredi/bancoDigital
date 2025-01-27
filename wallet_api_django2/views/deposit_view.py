# views/deposit.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from ..models import Transaction
from ..serializers import DepositSerializer

class DepositView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response(
                {"detail": "Depósito realizado com sucesso."},
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
            wallet.balance += amount
            wallet.save()

            Transaction.objects.create(
                sender=None,
                receiver=self.request.user,
                amount=amount,
                transaction_type='DEPOSIT',
                status='SUCCESS'
            )