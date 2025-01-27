from datetime import datetime, timedelta
from decimal import Decimal

from django.db import transaction as db_transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from wallet_api_django2.models import Transaction, User, Wallet
from wallet_api_django2.serializers import TransactionSerializer


class TransferView(APIView):
    def post(self, request):
        sender = request.user
        receiver_cpf = request.data.get('receiver_cpf')
        amount = request.data.get('amount')

        if not receiver_cpf or not amount:
            return Response({'error': 'CPF do destinatário e valor são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount_decimal = Decimal(amount)
            if amount_decimal <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response({'error': 'Valor inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        receiver = User.objects.filter(cpf=receiver_cpf).first()
        if not receiver:
            Transaction.objects.create(
                sender=sender,
                amount=amount_decimal,
                transaction_type='TRANSFER',
                status='FAILED'
            )
            return Response({'error': 'Destinatário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if sender == receiver:
            Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount_decimal,
                transaction_type='TRANSFER',
                status='FAILED'
            )
            return Response({'error': 'Não é possível transferir para si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                sender_wallet = Wallet.objects.select_for_update().get(user=sender)
                receiver_wallet = Wallet.objects.select_for_update().get(user=receiver)

                if sender_wallet.balance < amount_decimal:
                    Transaction.objects.create(
                        sender=sender,
                        receiver=receiver,
                        amount=amount_decimal,
                        transaction_type='TRANSFER',
                        status='FAILED'
                    )
                    return Response({'error': 'Saldo insuficiente.'}, status=status.HTTP_400_BAD_REQUEST)

                sender_wallet.balance -= amount_decimal
                sender_wallet.save()

                receiver_wallet.balance += amount_decimal
                receiver_wallet.save()

                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount_decimal,
                    transaction_type='TRANSFER',
                    status='SUCCESS'
                )
                return Response({'message': 'Transferência realizada com sucesso.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount_decimal,
                transaction_type='TRANSFER',
                status='FAILED'
            )
            return Response({'error': 'Erro na transferência.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionListView(APIView):
    def get(self, request):
        user = request.user
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        transactions = Transaction.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')

        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                transactions = transactions.filter(timestamp__range=[start, end])
            except ValueError:
                return Response({'error': 'Formato de data inválido. Use YYYY-MM-DD.'}, status=400)

        serializer = TransactionSerializer(transactions, many=True)
        return Response({'transactions': serializer.data})