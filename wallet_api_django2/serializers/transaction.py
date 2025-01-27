from rest_framework import serializers

from wallet_api_django2.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'transaction_type', 'status', 'timestamp']

    def get_sender(self, obj):
        return obj.sender.full_name if obj.sender else None

    def get_receiver(self, obj):
        return obj.receiver.full_name if obj.receiver else None