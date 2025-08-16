from django.contrib import admin
from .models import Wallet, Transaction, WithdrawalRequest

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance_usd", "referral_balance_ksh", "deposit_balance_ksh")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet", "amount", "currency", "transaction_type", "timestamp")
    list_filter = ("currency", "transaction_type")
    search_fields = ("wallets_user_username",)

@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ("wallet", "amount", "currency", "transaction_type", "timestamp")
    list_filter = ("transaction_type", "currency")
    search_fields = ("wallet__user__username",)
    

