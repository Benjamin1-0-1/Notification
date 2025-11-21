import uuid
from django.db import models
from .message import EmailMessage

RECIPIENT_TYPES = [
        ("to", "To"),
        ("cc", "Cc"),
        ("bcc", "Bcc"),
    ]

class EmailRecipient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_message = models.ForeignKey(
        EmailMessage,
        on_delete=models.CASCADE,
        related_name="recipients"
    )
    recipient_email = models.EmailField()
    type = models.CharField(max_length=10, choices=RECIPIENT_TYPES)

    def __str__(self):
        return f"{self.recipient_email} ({self.type})"