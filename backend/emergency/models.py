from django.db import models
from django.conf import settings
from django.utils import timezone

class EmergencyAlert(models.Model):
    ALERT_STATUS = (
        ('pending', 'Pending'),
        ('responding', 'Rresponding'),
        ('resolved', 'Resolved'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emergency_alerts')
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lng = models.DecimalField(max_length=9, decimal_places=6)
    messages = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=ALERT_STATUS, default='pending')
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Emergency Alert #{self.id} - {self.user.username}"

      