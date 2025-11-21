# Email Service app

This Django app exposes a simple service class and JSON API endpoint for sending
notification emails using the project-wide SMTP configuration.

## Service usage

```python
from email_service.services import send_notification_email

send_notification_email(
    subject='Greetings',
    recipients=['user@example.com'],
    text_template='email_service/example_email.txt',
    html_template='email_service/example_email.html',
    context={'name': 'Ada'},
)
```

You may omit the templates and instead pass `body='Plain text'`.

## HTTP endpoint

The `EmailNotificationView` is wired at `/api/email/send/`. POST JSON like:

```json
{
  "subject": "Test",
  "recipients": ["user@example.com"],
  "text_template": "email_service/example_email.txt",
  "html_template": "email_service/example_email.html",
  "context": {"name": "Ada"}
}
```

On success the endpoint returns `{"status": "sent", "delivered": 1}`.
