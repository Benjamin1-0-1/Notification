import africastalking
from django.conf import settings
from .base import SmsClient, SmsSendResult

class AfricasTalkingSmsClient(SmsClient):
    def __init__(self):
        africastalking.initialize(
            settings.AFRICASTALKING_USERNAME,
            settings.AFRICASTALKING_API_KEY
        )
        self.sms = africastalking.SMS

    def send_sms(self, to: str, body: str, sender_id=None) -> SmsSendResult:
        sender = sender_id or settings.AFRICASTALKING_SENDER_ID
        print("SENDER USED:", sender)

        try:            
            response = self.sms.send(body, [to], sender)
            print(response)
            message_data = response.get("SMSMessageData", {})
            recipients = message_data.get("Recipients", [])
            recipient = recipients[0] if recipients else {}
            status = recipient.get("status", "")
            status_code = str(recipient.get("statusCode", ""))
            message_id = recipient.get("messageId", "")
            success = status.lower() == "success"

            statuses = {"queued", "submitted", "buffered"}
            is_retryable = status.lower() in statuses

            return SmsSendResult(
                success=success,
                status=status,
                provider_message_id=message_id,
                error_code=None if success else status_code,
                error_message=None,
                is_retryable=is_retryable
            )

        except Exception as exc:
            return SmsSendResult(
                success=False,
                status="Exception",
                error_code="exception",
                error_message=str(exc),
                is_retryable=True
            )
