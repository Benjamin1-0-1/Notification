from django.http import JsonResponse
from auth_service.models import User, OTP
from auth_service.services.otp import create_otp
from auth_service.services.jwt import generate_jwt
from django.utils import timezone
from auth_service.kafka.producer import publish_event



def register(request):
    phone = request.POST.get("phone")
    user, _ = User.objects.get_or_create(phone=phone)
    otp_code = create_otp(user)

    publish_event("auth.otp.requested", {
        "phone": phone,
        "otp": otp_code
    })

    return JsonResponse({"message": "OTP sent to your phone number"})


def verify(request):
    phone = request.POST.get("phone")
    otp_input = request.POST.get("otp")
    user = User.objects.get(phone=phone)
    otp = OTP.objects.filter(user=user, is_used=False).latest("id")

    if otp.expires_at < timezone.now():
        return JsonResponse({"error": "Sorry,the has OTP expired"}, status=400)
    if otp.code != otp_input:
        return JsonResponse({"error": "Invalid OTP.Please try agin orrequest another OTP."}, status=400)

    otp.is_used = True
    otp.save()
    user.is_verified = True
    user.save()
    token = generate_jwt(user.id)

    return JsonResponse({"token": token})
