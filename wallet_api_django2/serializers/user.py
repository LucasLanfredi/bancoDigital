from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['cpf', 'full_name', 'password']

    def validate_cpf(self, value):
        """
        Valida se o CPF já está cadastrado.
        """
        if User.objects.filter(cpf=value).exists():
            raise serializers.ValidationError("CPF já cadastrado.")
        return value

    def create(self, validated_data):
        """
        Cria o usuário com os dados validados.
        """
        try:
            user = User.objects.create_user(
                cpf=validated_data['cpf'],
                full_name=validated_data['full_name'],
                password=validated_data['password']
            )
            return user
        except IntegrityError as e:
            raise serializers.ValidationError({"cpf": "Erro ao criar usuário. CPF já cadastrado."})