from django.contrib.auth.models import AbstractUser
from django.db import models
from packages.models import Package
import uuid
from django.utils import timezone
from datetime import timedelta, date

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    package = models.OneToOneField(Package, null=True, blank=True, on_delete=models.SET_NULL)
    referral = models.CharField(max_length=100, unique=True, blank=True, null=True)
    friends = models.JSONField(default=list, blank=True)
    subscription_start = models.DateField(null=True, blank=True)
    subscription_end = models.DateField(null=True, blank=True)
    is_active_subscription = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Generate referral code if not present
        if not self.referral:
            self.referral = self.generate_referral_code()

        # Update subscription dates if a package is assigned
        if self.package:
            if not self.subscription_start:
                self.subscription_start = date.today()
            self.subscription_end = self.subscription_start + timedelta(days=self.package.length)

        # Update active subscription status
        if self.subscription_end and self.subscription_end >= date.today():
            self.is_active_subscription = True
        else:
            self.is_active_subscription = False

        super().save(*args, **kwargs)
        
    def generate_referral_code(self):
        return str(uuid.uuid4())[:8]

    @property
    def subscription_progress(self):
        if self.subscription_start and self.subscription_end:
            total_days = (self.subscription_end - self.subscription_start).days
            days_passed = (timezone.now().date() - self.subscription_start).days
            return (days_passed / total_days) * 100
        return 0

    @property
    def days_passed(self):
        if self.subscription_start:
            return (timezone.now().date() - self.subscription_start).days
        return 0

    @property
    def days_left(self):
        if self.subscription_end:
            return (self.subscription_end - timezone.now().date()).days
        return 0
    @property
    def total_days(self):
        if self.subscription_start and self.subscription_end:
            return (self.subscription_end - self.subscription_start).days
        return 0