# SMS Service Guide

This document explains how `sms_service` sends SMS, how OTP SMS works end-to-end, the routes involved, and how to test locally.

## 1) What `sms_service` does

`sms_service` is the SMS delivery layer for this project.

Main responsibilities:
- Normalize phone numbers to Kenya format (`+2547...`).
- Check opt-in status (`SmsOptIn`).
- Send SMS through Africa's Talking.
- Persist each attempt in `SmsMessage` with provider metadata.

Core files:
- `sms_service/views.py`
- `sms_service/urls.py`
- `sms_service/services/sms_service.py`
- `sms_service/services/clients/afrtalking_client.py`
- `sms_service/models.py`

## 2) How SMS is requested

### A. Direct function call (core path)

Call the service instance:

```python
from sms_service.services.sms_service import sms_service

sms = sms_service.send_sms(
    to="+254700000000",
    body="Your OTP code is 123456",
    sender_id=None,
)
```

What happens internally:
1. `SmsService.normalize_phone(to)` standardizes the phone number.
2. `SmsOptIn.objects.get_or_create(phone_number=phone)` checks/creates opt-in row.
3. If opted out, returns a saved `SmsMessage` with status `BLOCKED_OPTOUT`.
4. Calls provider client: `AfricasTalkingSmsClient.send_sms(...)`.
5. Maps provider result to local status:
- `success=True` -> `ACCEPTED`
- `is_retryable=True` -> `THROTTLED`
- otherwise -> `FAILED`
6. Saves and returns `SmsMessage`.

Saved fields include:
- `to`
- `body`
- `sender_id`
- `status`
- `provider_message_id`
- `provider_status`
- `error_code`
- `error_message`
- `sent_at`

### B. HTTP test request route

Route:
- `GET /sms/test/`

View:
- `send_test_sms` in `sms_service/views.py`

Response shape:

```json
{
  "to": "+254700000000",
  "status": "ACCEPTED",
  "provider_message_id": "ATXid_..."
}
```

Error response:

```json
{
  "error": "..."
}
```

Notes:
- The route is intended for test traffic.
- Current code builds and sends the SMS before checking request method.

## 3) Callback URLs and callback response data

Current implementation status:
- There is **no callback/webhook URL** for Africa's Talking delivery reports in this repo.
- No Django route currently receives provider delivery callbacks.

What is currently captured:
- Immediate provider API response fields parsed in `AfricasTalkingSmsClient.send_sms(...)`:
- `status`
- `statusCode`
- `messageId`

These are stored on `SmsMessage` as:
- `provider_status`
- `error_code`
- `provider_message_id`

If you need callback support, add a new URL + view in `sms_service` to receive delivery reports and update `SmsMessage` (for example by `provider_message_id`).

## 4) OTP flow (end-to-end process)

OTP is initiated by `auth_service` and delivered by `sms_service` through Kafka.

### Routes involved
- `POST /auth_service/register/` -> creates/gets user, creates OTP, publishes Kafka event.
- `POST /auth_service/verify/` -> checks OTP and returns JWT token.
- `GET /sms/test/` -> standalone SMS test route.

### OTP request sequence

1. Client sends phone number to `POST /auth_service/register/`.
2. `auth_service.views.register`:
- reads `phone` from `request.POST`
- creates/gets `User`
- generates and stores OTP via `create_otp(user)`
- publishes Kafka event:

```json
{
  "phone": "+254700000000",
  "otp": "123456"
}
```

3. `auth_service/kafka/consumer.py` listens to topic `auth.otp.requested`.
4. Consumer builds SMS text and calls:

```python
sms_service.send_sms(phone, f"Your OTP code is {otp}. It expires in 5 minutes.")
```

5. SMS attempt is saved in `SmsMessage`.

### Register response

Success:

```json
{
  "message": "OTP sent to your phone number"
}
```

### Verify request + response

Request form fields:
- `phone`
- `otp`

Success response:

```json
{
  "token": "<jwt_token>"
}
```

Possible error responses:

```json
{
  "error": "Sorry,the has OTP expired"
}
```

```json
{
  "error": "Invalid OTP.Please try agin orrequest another OTP."
}
```

## 5) Routes summary

Project URL mapping (`NotificationService/urls.py`):
- `sms/` -> `sms_service.urls`
- `auth_service/` -> `auth_service.urls`

Effective routes:
- `GET /sms/test/`
- `POST /auth_service/register/`
- `POST /auth_service/verify/`

## 6) Local setup and testing

## Prerequisites
- Python 3.11+
- Docker (for Kafka + Zookeeper)

Install dependencies:

```bash
pip install -r requirements.txt
```

Create env file (project root `.env`) using values from `sms_service/.env.example`:

```env
AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY=<your_key>
AFRICASTALKING_SENDER_ID=
```

Run migrations:

```bash
python manage.py migrate
```

### Start Kafka stack

```bash
docker compose up -d zookeeper kafka
```

### Start Django API

```bash
python manage.py runserver
```

### Start OTP Kafka consumer (new terminal)

```bash
python auth_service/kafka/consumer.py
```

### Test SMS directly

```bash
curl http://127.0.0.1:8000/sms/test/
```

### Test OTP flow

1. Request OTP:

```bash
curl -X POST http://127.0.0.1:8000/auth_service/register/ -d "phone=+254700000000"
```

2. Wait for consumer to process message (check consumer terminal log).
3. Verify OTP:

```bash
curl -X POST http://127.0.0.1:8000/auth_service/verify/ -d "phone=+254700000000" -d "otp=<code>"
```

## 7) Quick troubleshooting

- If OTP is not sent, confirm Kafka is running and `auth_service/kafka/consumer.py` is active.
- If SMS fails, check Africa's Talking env variables.
- If verify fails, confirm OTP has not expired (5 minutes) and the latest OTP is used.