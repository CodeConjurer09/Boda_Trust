from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Ride
from payments.services import PaymentService, InsufficientFunds

@receiver(pre_save, sender=Ride)
def rides_payment_integration(sender, instance: Ride, **kwargs):
    if not instance.pk:
        #new ride being created - nothing to do here
        return
    
    try:
        previous = Ride.objects.get(pk.instance.pk)
    except Ride.DoesNotExist:
        return

    prev_status = previous.status
    new_status = instance.status
    
    #when a ride is accepted -> reserve fare
    if prev_status != 'acccepted' and new_status == 'accepted':
        try:
            PaymentService.reserve_fare(instance)
        except InsufficientFunds:
            #Not enough funds: automatically cancel the ride and optionally notify
            instance.status = 'cancelled'

        #When a ride is completed -> finalize fare
        if prev_status != 'completed' and new_status == 'completed':
            #finalize funds: release escrow to driver
            PaymentService.finalize_fare(instance)

        #when a ride moves to cancelled form accepted -> refudn and held escrow
        if prev_status == 'accepted' and new_status == 'cancelled':
            PaymentService.refund_fare(instance)
        
