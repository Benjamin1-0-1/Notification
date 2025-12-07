from dataclasses import dataclass
from typing import Optional


@dataclass
class SmsSendResult:
    success: bool
    status: str
    provider_message_id: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    is_retryable: bool = False


class SmsClient:
    def send_sms(self, to: str, body: str, sender_id: Optional[str] = None) -> SmsSendResult:
        raise NotImplementedError
