import re
from django.utils import timezone
from sms_service.models import SmsMessage, SmsOptIn, SmsMessageStatus
from .clients.afrtalking_client import AfricasTalkingSmsClient


class SmsService:
    def __init__(self):
        self.client = AfricasTalkingSmsClient()

    def normalize_phone(self, phone: str) -> str:
        # force digits only
        digits = re.sub(r"\D", "", phone)

        #No format
        if digits.startswith("0"):
            digits = "254" + digits[1:]
        if digits.startswith("7"):
            digits = "254" + digits

        return f"+{digits}"

    def send_sms(self, to: str, body: str, sender_id=None):
        phone = self.normalize_phone(to)

        opt, _ = SmsOptIn.objects.get_or_create(phone_number=phone)
        if not opt.is_opted_in:
            return SmsMessage.objects.create(
                to=phone,
                body=body,
                status=SmsMessageStatus.BLOCKED_OPTOUT
            )

        result = self.client.send_sms(phone, body, sender_id)

        if result.success:
            status = SmsMessageStatus.ACCEPTED
        elif result.is_retryable:
            status = SmsMessageStatus.THROTTLED
        else:
            status = SmsMessageStatus.FAILED

        #save to db
        return SmsMessage.objects.create(
            to=phone,
            body=body,
            sender_id=sender_id or "",
            status=status,
            provider_message_id=result.provider_message_id or "",
            provider_status=result.status,
            error_code=result.error_code or "",
            error_message=result.error_message or "",
            sent_at=timezone.now(),
        )


sms_service = SmsService()
