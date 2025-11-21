import uuid
from django.db import models
from .message import EmailMessage


class EmailHeader(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_message = models.ForeignKey(
        EmailMessage,
        on_delete=models.CASCADE,
        related_name="headers"
    )
    header_name = models.CharField(max_length=255)
    header_value = models.TextField()

    def __str__(self):
        return f"{self.header_name}"
