import uuid
from django.db import models

STATUS_CHOICES = [
        ("queued", "Queued"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

class EmailMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=255)
    from_email = models.EmailField()
    body_text = models.TextField(blank=True, null=True)
    body_html = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="queued")
    error_message = models.TextField(blank=True, null=True)
    retry_count = models.PositiveIntegerField(default=0)

    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} ({self.status})"
