from django.db import models
from django.conf import settings
from django.utils import timezone

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    escrow_usd = models.DecimalField(max_length=12, decimal_places=2, default=0.00)
    referral_balance_ksh = models.DecimalField(max_length=10, decimal_places=2, default=0.00)
    deposit_balance_ksh = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        uname = getattr(self.user, 'username', None) or getattr(self.user, 'email', str(self.user))
        return f"Wallet of {uname}"
    
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ("hold", "Hold"),
        ("release", "Release"),
        ('purchase', 'Purchase'),
        ("driver_payout", "Driver Payout"),
        ('referral_earning', 'Referral Earning'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_fields='withdrawal_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[("USD", "USD"), ("KES", "KES")], default="USD")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    related_object_type = models.CharField(max_length=50, blank=True, null=True) # eg Ride 
    related_object_id = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency}"
    

class WithdrawalRequest(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="withdrawal_requests")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[("USD", "USD"), ("KSH", "KSH")])
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending")
    request_date = models.DateTimeField(default=timezone.now)
    processed_date = models.DateTimeField(blank=True, null=True)

    def approve(self):
        self.status = "approved"
        self.processed_date = timezone.now()
        self.save()

    def reject(self):
        self.status = "rejected"
        self.processed_date = timezone.now()
        self.save()

    def __str__(self):
        return f"Withdrawal {self.amount} {self.currency} - {self.status}"
