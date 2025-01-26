from decimal import Decimal

from rest_framework import serializers
from ..models import Transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'sender_cpf',
            'receiver_cpf',
            'amount',
            'transaction_type',
            'status',
            'timestamp'
        )
        read_only_fields = ('status', 'timestamp')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['cpf'] = self.user.cpf
        data['full_name'] = self.user.full_name
        return data

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal(0.01))