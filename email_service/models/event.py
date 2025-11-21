import uuid
from django.db import models
from .message import EmailMessage

EVENT_TYPES = [
        ("open", "Open"),
        ("click", "Click"),
        ("bounce", "Bounce"),
        ("delivered", "Delivered"),
    ]

class EmailEvent(models.Model):    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_message = models.ForeignKey(
        EmailMessage,
        on_delete=models.CASCADE,
        related_name="events"
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} event"
