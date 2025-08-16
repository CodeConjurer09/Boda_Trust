from rest_framework import generics, permissions
from .models import Wallet, Transaction, WithdrawalRequest
from .serializers import WalletSerializer, TransactionSerializer, WithdrawalRequestSerializer

class WalletCreateView(generics.CreateAPIView):
    queryset = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Wallet.objects.get_or_delete(user=self.request.user)[0]
    

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wallet = Wallet.objects.get_or_delete(user=self.request.user)
        return wallet.transactions.all()
    
class WithdrawalRequestListView(generics.ListAPIView):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        wallet = Wallet.objects.get_or_create(user=self.request.user)
        serializer.save(wallet=wallet)

        