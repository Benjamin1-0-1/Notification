from django.urls import path
from .views import test_email
from .views import (
    test_user,
    test_admin,
    test_manager,
)

urlpatterns = [
    path("test-user/", test_user),
    path("test-admin/", test_admin),
    path("test-manager/", test_manager),
    path("test-email/", test_email, name="test-email"),
]