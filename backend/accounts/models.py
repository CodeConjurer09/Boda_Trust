from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email, phone_number=None, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, passowrd=password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model used across the project.

    Important fields:
    - email: primary identifier
    - is_driver: flag to separate driver/passenger behaviors
    - location: GeoDjango PointField (for drivers)
    - kyc_document / is_verified: for driver verification
    """
    #Core
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=24, unique=True, error_messages={'unique': 'This number is already in use.'})
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    # Roles & Flags
    is_driver = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False) #KYC approved
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # location(for drivers) - Geodjango PointField
    location = geomodels.PointField(null=True, blank=True, geography=True)

    # KYC documents and metadata
    kyc_document = models.FileField(upload_to='kyc_docs/', null=True, blank=True)
    kyc_verified_at = models.DateTimeField(null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
        