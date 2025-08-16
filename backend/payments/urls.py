from django.urls import path
from .views import WalletView, TransactionListView, WithdrawalRequestCreateView

urlpatterns = [
    path("wallet/", WalletView.as_view(), name="wallet_detail"),
    path("transactions/", TransactionListView.as_view(), name="transaction_list"),
    path("withdrawal/", WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
]