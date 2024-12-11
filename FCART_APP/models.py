from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=12, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default=None, )
    address = models.CharField(max_length=50)
    verify_through = models.CharField(max_length=50, choices=[('Mobile_SMS', 'Mobile SMS'), ('Email', 'Email'), ('call', 'call')], default='OTP',)
    role = models.CharField(max_length=100, choices=[('Customer', 'Customer'), ('Seller', 'Seller'), ('Admin', 'Admin')], default="Customer")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='fcartapp_user_set',  # Custom related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='fcartapp_user_permissions_set',  # Custom related_name
        blank=True,
    )
    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = ["password"]
