from django.db import models
from django.db import models
from django.utils import timezone

class SmsMessageStatus(models.TextChoices):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    FAILED = "FAILED"
    THROTTLED = "THROTTLED"
    DELIVERED = "DELIVERED"
    BLOCKED_OPTOUT = "BLOCKED_OPTOUT"

class SmsOptIn(models.Model):
    phone_number = models.CharField(max_length=32, unique=True)
    is_opted_in = models.BooleanField(default=True)
    opted_out_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.phone_number} ({'opted-in' if self.is_opted_in else 'opted-out'})"

class SmsMessage(models.Model):
    to = models.CharField(max_length=32)
    body = models.TextField()
    sender_id = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=32, choices=SmsMessageStatus.choices)
    provider_message_id = models.CharField(max_length=128, blank=True)
    provider_status = models.CharField(max_length=64, blank=True)
    error_code = models.CharField(max_length=64, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def mark_delivered(self):
        self.status = SmsMessageStatus.DELIVERED
        self.delivered_at = timezone.now()
        self.save()

    def __str__(self):
        return f"SMS to {self.to} [{self.status}]"
