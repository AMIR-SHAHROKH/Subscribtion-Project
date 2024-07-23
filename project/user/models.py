from django.contrib.auth.models import AbstractUser
from django.db import models
from packages.models import Package
import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    packages = models.OneToOneField(Package, null=True, blank=True, on_delete=models.SET_NULL)
    referral = models.CharField(max_length=100, unique=True, blank=True, null=True)
    friends = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.referral:
            self.referral = self.generate_referral_code()
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        return str(uuid.uuid4())[:8] 
