# NotificationService

Django 5.2 project providing email and SMS notification services with Africa's Talking SMS integration and templated emails.

## Project Structure
- `NotificationService/` – project config (`settings.py`, `urls.py`, `wsgi.py`).
- `email_service/` – email models, service layer, demo views, and templates.
- `sms_service/` – SMS models, Africa's Talking client, service layer, and demo view.
- `.env` – environment variables (not committed).
- `db.sqlite3` – local SQLite database.
- `manage.py` – Django entry point.

## Requirements
- Python 3.10+ recommended
- Key packages: `Django==5.2.8`, `africastalking==2.0.1`, `python-dotenv`, `requests`, `PyYAML`
- Install: `pip install Django==5.2.8 africastalking==2.0.1 python-dotenv requests PyYAML`

## Environment Variables
Set these in `.env` (loaded via `python-dotenv` in `NotificationService/settings.py`):
- `AFRICASTALKING_USERNAME` (default: `sandbox`)
- `AFRICASTALKING_API_KEY`
- `AFRICASTALKING_SENDER_ID`
- `DJANGO_EMAIL_BACKEND` (default: `django.core.mail.backends.console.EmailBackend`)
- `DJANGO_EMAIL_HOST`, `DJANGO_EMAIL_PORT`, `DJANGO_EMAIL_HOST_USER`, `DJANGO_EMAIL_HOST_PASSWORD`
- `DJANGO_EMAIL_USE_TLS` (`true`/`false`, default `false`)
- `DJANGO_DEFAULT_FROM_EMAIL` (default: `Areris World Service <arerisworld@gmail.com>`)

## Setup & Run
1) Create venv: `python -m venv .venv && .\.venv\Scripts\activate`
2) Install deps (see above).
3) Apply migrations: `python manage.py migrate`
4) Run server: `python manage.py runserver`

## Email Service (`email_service`)
- Core service: `email_service/services.py::EmailService`
  - `queue_template_email(subject, to, template_path, context, from_email=None, cc=None, bcc=None)` renders `emails/{template_path}.txt` and `.html`, persists `EmailMessage` + `EmailRecipient` records.
  - `send_email(email_message_id)` builds `EmailMultiAlternatives`, attaches HTML/attachments/headers, sends via configured backend, and updates status.
- Models: `EmailMessage`, `EmailRecipient`, `EmailHeader`, `EmailAttachment`, `EmailEvent` (`email_service/models/*.py`).
- Templates: `email_service/templates/emails/`
  - `base.html`
  - `user/welcome.(html|txt)`
  - `admin/new_user.(html|txt)`
  - `manager/task.(html|txt)`, `manager/report.(html|txt)`
- Demo endpoints (`email_service/urls.py`):
  - `GET /email/test-email/` – simple plain+HTML example.
  - `GET /email/test-user/` – user welcome template.
  - `GET /email/test-admin/` – admin new-user alert template.
  - `GET /email/test-manager/` – manager task assignment template.
- Usage example:
  ```python
  from email_service.services import EmailService

  email_msg = EmailService.queue_template_email(
      subject="Welcome",
      to=["user@example.com"],
      template_path="user/welcome",
      context={"user": {"first_name": "Ada", "email": "user@example.com"}},
      from_email="no-reply@example.com",
  )
  EmailService.send_email(email_msg.id)
  ```

## SMS Service (`sms_service`)
- Core service: `sms_service/services/sms_service.py::SmsService`
  - Normalizes phone numbers to `+2547xxxxxxx` style.
  - Honors opt-in status via `SmsOptIn`; returns `BLOCKED_OPTOUT` if opted out.
  - Sends through Africa's Talking via `AfricasTalkingSmsClient` (`sms_service/services/clients/afrtalking_client.py`), mapping provider status to local `SmsMessageStatus`.
- Models (`sms_service/models.py`): `SmsMessageStatus` enum, `SmsOptIn`, `SmsMessage` (with delivery timestamps and provider metadata).
- Demo endpoint (`sms_service/urls.py`):
  - `GET /sms/test/` – sends a test SMS using Africa's Talking credentials.
- Direct use:
  ```python
  from sms_service.services.sms_service import sms_service

  sms = sms_service.send_sms("+254700000000", "Hello from Django + Africa's Talking")
  print(sms.status, sms.provider_message_id)
  ```

## Running Demo Endpoints
- Start server: `python manage.py runserver`
- Email demos: visit `/email/test-email/`, `/email/test-user/`, `/email/test-admin/`, `/email/test-manager/`
- SMS demo: visit `/sms/test/` (requires valid Africa's Talking sandbox or live credentials)

## Notes
- Database: SQLite by default (`db.sqlite3`); adjust `DATABASES` in `NotificationService/settings.py` for production.
- Attachments/headers are modeled but expect storage/backends to be configured for production email delivery.
- For production, ensure `DEBUG=False`, set `ALLOWED_HOSTS`, and use a real SMTP backend.
