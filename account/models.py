from django.db import models
from account.managers import *
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserAccount(AbstractBaseUser, PermissionsMixin):
    USER_TYPE =[
        ('User', 'User'),
        ('Admin', 'Admin'),
    ]
    email = models.EmailField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=255, choices=USER_TYPE, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email