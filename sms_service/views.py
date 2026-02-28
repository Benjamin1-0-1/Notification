from django.http import JsonResponse
from sms_service.services.sms_service import sms_service


def send_test_sms(request):
    sms = sms_service.send_sms(
        "+254700000000",
        "This is a test SMS from Africa's Talking Django service."
    )
    return JsonResponse({
        "to": getattr(sms, "to", None),
        "status": getattr(sms, "status", None),
        "provider_message_id": getattr(sms, "provider_message_id", None),
    })
