from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    BalanceView,
    DepositView,
    TransferView,
    TransactionListView,
    WithdrawView
)

urlpatterns = [
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),

    path('api/wallets/balance/', BalanceView.as_view(), name='balance'),
    path('api/wallets/deposit/', DepositView.as_view(), name='deposit'),

    path('api/transactions/', TransferView.as_view(), name='transfer'),
    path('api/transactions/history/', TransactionListView.as_view(), name='transactions'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
]