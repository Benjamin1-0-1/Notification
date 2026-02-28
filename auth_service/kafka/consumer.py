import os
import sys
from pathlib import Path
import json

# Add project root (folder that contains manage.py) to sys.path
ROOT_DIR = Path(__file__).resolve().parents[2]  # kafka -> auth_service -> Not_ser
sys.path.insert(0, str(ROOT_DIR))

# Boot Django so apps can be imported
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NotificationService.settings")

import django
django.setup()

# ✅ Import the sms_service instance
from sms_service.services.sms_service import sms_service

from kafka import KafkaConsumer

TOPIC = "auth.otp.requested"

def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="notification-service",
    )

    print(f"✅ Listening on topic: {TOPIC}")

    for msg in consumer:
        payload = msg.value
        phone = payload.get("phone")
        otp = payload.get("otp")

        if not phone or not otp:
            print("⚠️ Invalid payload:", payload)
            continue

        text = f"Your OTP code is {otp}. It expires in 5 minutes."
        saved = sms_service.send_sms(phone, text)

        print(f"📨 Sent OTP to {phone} | status={saved.status}")

if __name__ == "__main__":
    main()
