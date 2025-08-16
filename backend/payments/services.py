from decimal import Decimal
from django.conf import settings
from django.db import transaction
from .models import Wallet, Transaction

class InsufficientFunds(Exception):
    pass 

class PaymentService:
    @staticmethod
    def get_wallet(user):
        wallet, _ = Wallet.objects.get_or_create(user=user)
        return wallet
    
    @staticmethod
    def usd_to_ksh(usd_amount: Decimal) -> Decimal:
        rate = Decimal(getattr(settings, 'KSH_PER_USD', 140))
        return (usd_amount * rate).quantize(Decimal('0.01'))

    @staticmethod
    @transaction.atomic
    def reserve_fare(ride):
        """Reserve fare from passenger's USD wallet (move from balance_usd -> escrow_usd).
        Creates a Transaction of type 'hold'.

        Raises InsufficientFunds if passenger has not enough USD.
        """
        passenger = ride.passenger
        fare = Decimal(ride.fare or 0)
        wallet = PaymentService.get_wallet(passenger)

        if wallet.balance_usd < fare:
            raise InsufficientFunds(F"Passenger {passenger} has insufficient funds to reserve fare of {fare} USD, available {wallet.balance_usd}")

        wallet.balance_usd -= fare
        wallet.escrow_usd += fare 
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            amount=fare,
            currency='USD',
            transaction_type='hold',
            related_object_type='Ride',
            related_object_id=(ride.id),
            description=f"Fare held for ride {ride.id}"
        )

    @staticmethod
    @transaction.atomic
    def finalize_fare(ride):
        """Finalize fare after ride completion: move escrow to driver's wallet and create transactions.
        Also handles referral commission for the passenger's referrer if applicable.
        """
        passenger = ride.passenger
        driver = ride.driver
        fare = Decimal(ride.fare or 0)

        passenger_wallet = PaymentService.get_wallet(passenger)
        driver_wallet = PaymentService.get_wallet(driver)

        #ensure escrow exists
        if passenger_wallet.escrow_usd < fare:
            raise Exception(f"Escrow for passenger {passenger} insufficient: has {passenger_wallet.escrow_usd}, expected {fare}")

        #move out of escrow
        passenger_wallet.escrow_usd -= fare
        passenger_wallet.save()

        #platform fee logic. for we assume no fee, or you can set platform_fee_percent in settings
        platform_fee_payment = Decimal(getattr(settings, 'PLATFORM_FEE_PERCENT', 0))
        platform_fee = (fare * platform_fee_payment).quantize(Decimal('0.01'))
        driver_payout = (fare - platform_fee).quantize(Decimal('0.01'))
        #credit driver
        driver_wallet.balance_usd += driver_payout
        driver_wallet.save()

        #create transactions 
        Transaction.objects.create(
            wallet=passenger_wallet,
            amount=fare,
            currency='USD',
            transaction_type='purchase',
            related_object_type='Ride',
            related_object_id=str(ride.id),
            description=f'Fare paid for ride {ride.id}',
        )
        Transaction.objects.create(
            wallet=driver_wallet,
            amount=driver_payout,
            currency='USD',
            transaction_type='driver_payout',
            related_object_type='Ride',
            related_object_id=str(ride.id),
            description=f'Payout for ride {ride.id}',
        )

        if platform_fee > 0:
            #optional create a platform fee transaction(could be credited to a platform wallet)
            Transaction.objects.create(
                wallet=driver_wallet, #or a specific platform wallet
                amount=platform_fee,
                currency='USD',
                transaction_type='withdrawal',
                related_object_type='Ride',
                related_object_id=str(ride.id),
                description=f'Platform fee for ride {ride.id}',
            )

            #handle referral commission if passenger has a referrer|(one time on first paid ride)
            try:
                from referrrals.models import Referral #optional app;import lazily
            except Exception:
                Referral = None
                if Referral is not None:
                    #check is passenger has a referrer and if this is the first paid
                    ref = Referral.objects.filter(referred_user=passenger, rewarded=False).first()
                    if ref is not None:
                        # compute referral amount (10% of fare) and credit to referrer in KSH
                        referral_percent = Decimal(getattr(settings, 'REFERRAL_PERCENT', 0.10))
                        referral_amount_usd = (fare * referral_percent).quantize(Decimal('0.01'))
                        referral_amount_ksh = PaymentService.usd_to_ksh(referral_amount_usd)

                        ref_wallet = PaymentService.get_wallet(ref.referrer)
                        ref_wallet.referral_balance_ksh += referral_amount_ksh
                        ref_wallet.save()

                        Transaction.objects.create(
                            wallet=ref_wallet,
                            amount=referral_amount_ksh,
                            currency='KSH',
                            transaction_type='referral_earning',
                            related_object_type='Referral',
                            related_object_id=str(ride.id),
                            description=f' Referral commission for referring {passenger.email} on ride {ride.id}'
                        )
                        #mark as rewarded
                        ref.rewarded = True
                        ref.save()

    @staticmethod
    @transaction.atomic
    def refund_fare(ride):
        """Refund the fare back to passenger's USD balance from escrow (used when ride is cancelled after hold).
        """
        passenger = ride.passenger
        fare = Decimal(ride.fare or 0)
        wallet = PaymentService.get_wallet(passenger)

        if wallet.escrow_usd < fare:
            #partial or no escrow attempt to refund whatever is in escrow
            refund_amount = wallet.escrow_usd
        else:
            refund_amount = fare

        wallet.escrow_usd -= refund_amount
        wallet.balance_usd += refund_amount
        wallet.save()
        #create refund transaction
        Transaction.objects.create(
            wallet=wallet,
            amount=refund_amount,
            currency='USD',
            transaction_type='release',
            related_object_type='Ride',
            related_object_id=str(ride.id),
            description=f'Refund for cancelled ride {ride.id}'
        )