import uuid
from django.db import models
from .message import EmailMessage

class EmailAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_message = models.ForeignKey(
        EmailMessage,
        on_delete=models.CASCADE,
        related_name="attachments"
    )
    file_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    file = models.FileField(upload_to="email_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
