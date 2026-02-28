import random
import hashlib
from django.utils import timezone
from datetime import timedelta
from auth_service.models import OTP

def generate_otp():
    return str(random.randint(100000, 999999))


def create_otp(user):
    code = generate_otp()
    OTP.objects.create(
        user=user,
        code=code,
        expires_at=timezone.now() + timedelta(minutes=5)
    )
    return code
