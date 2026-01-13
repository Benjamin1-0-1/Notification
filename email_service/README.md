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


# Email Service – Architecture & Request Flow

This module provides a structured, auditable, and scalable email-sending system
for the Django project. Emails are treated as first-class records in the database,
allowing tracking, retries, analytics, and future async processing.

---

## 1. High-Level Overview

An email request in this system follows **three major phases**:

1. **Preparation (queueing)**
2. **Sending**
3. **Post-send tracking**

At no point is an email sent without first being persisted in the database.

---
