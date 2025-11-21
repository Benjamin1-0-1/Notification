from django.http import JsonResponse
from .services import EmailService


def test_email(request):
    # 1. Queue email
    email_message = EmailService.queue_email(
        subject="Hello Django!",
        to=["test@example.com"],
        body_text="This is a plain text message",
        body_html="<h1>Hello Django!</h1><p>This is an HTML email.</p>",
        from_email="arerisworld@gmail.com",
    )

    EmailService.send_email(email_message.id)

    return JsonResponse({"message": "Email sent!"})

def test_user(request):
    user = {
        "first_name": "Ben",
        "email": "ben@example.com"
    }

    email_msg = EmailService.queue_template_email(
        subject="Welcome, Ben!",
        to=["ben@example.com"],
        template_path="user/welcome",
        context={"user": user},
        from_email="your_email@gmail.com"
    )

    EmailService.send_email(email_msg.id)
    return JsonResponse({"message": "User welcome email sent!"})

def test_admin(request):
    admin = {"email": "admin@example.com"}
    #WE CAN USE USER DATA FROM A DB 
    user = {
        "full_name": "New User",
        "email": "newuser@example.com"
    }

    email_msg = EmailService.queue_template_email(
        subject="A New User Has Registered",
        to=["admin@example.com"],
        template_path="admin/new_user",
        context={"user": user, "created_at": "2024-02-01"},
        from_email="your_email@gmail.com"
    )

    EmailService.send_email(email_msg.id)
    return JsonResponse({"message": "Admin email sent!"})

def test_manager(request):
    manager = {"name": "Manager John", "email": "manager@example.com"}
    task = {
        "title": "Approve Budget",
        "description": "Review and approve the Q1 budget.",
        "deadline": "2024-03-01",
    }

    email_msg = EmailService.queue_template_email(
        subject="New Task Assigned",
        to=["manager@example.com"],
        template_path="manager/task",
        context={"manager": manager, "task": task},
        from_email="your_email@gmail.com"
    )

    EmailService.send_email(email_msg.id)
    return JsonResponse({"message": "Manager task email sent!"})
