from django.urls import path
from .views import send_test_sms
urlpatterns = [
    path("test/" ,send_test_sms),
]
