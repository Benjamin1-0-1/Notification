from django.urls import path
from .views import register, verify

urlpatterns = [
    path("register/", register),
    path("verify/", verify),
]
