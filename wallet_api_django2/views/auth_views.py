from rest_framework import generics, permissions  # Adicione esta importação
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models import User
from ..serializers import UserSerializer, CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer