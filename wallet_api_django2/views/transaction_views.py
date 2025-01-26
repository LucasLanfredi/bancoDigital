from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models, transaction
from datetime import datetime
from ..models import Transaction
from ..serializers import TransactionSerializer

class TransferView(generics.CreateAPIView):
    """
    Endpoint para realizar transferências entre usuários.
    Requer autenticação JWT.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender = self.request.user
        receiver = serializer.validated_data['receiver']
        amount = serializer.validated_data['amount']

        # Validações
        if sender == receiver:
            return Response(
                {'detail': 'Não é possível transferir para si mesmo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if sender.wallet.balance < amount:
            return Response(
                {'detail': 'Saldo insuficiente para realizar a transferência.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Processamento da transferência
        with transaction.atomic():
            try:
                # Atualizar saldos
                sender.wallet.balance -= amount
                sender.wallet.save()

                receiver.wallet.balance += amount
                receiver.wallet.save()

                # Registrar transação
                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    transaction_type='TRANSFER',
                    status='SUCCESS'
                )

                return Response(
                    {
                        'detail': 'Transferência realizada com sucesso.',
                        'new_balance': sender.wallet.balance
                    },
                    status=status.HTTP_201_CREATED
                )

            except Exception as e:
                # Registrar falha na transação
                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    transaction_type='TRANSFER',
                    status='FAILED'
                )
                return Response(
                    {'detail': f'Erro ao processar transferência: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

class TransactionListView(generics.ListAPIView):
    """
    Endpoint para listar transações de um usuário.
    Permite filtro por período.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        )

        # Filtro por datas
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                queryset = queryset.filter(timestamp__date__range=[start, end])
            except ValueError:
                return Transaction.objects.none()

        return queryset.order_by('-timestamp')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        # Adiciona saldo atual ao retorno
        response.data['current_balance'] = request.user.wallet.balance
        return response