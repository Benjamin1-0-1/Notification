from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models.recipient import EmailRecipient
from .models.message import EmailMessage

class EmailService:
    @staticmethod
    def send_email(email_message_id: str):
        try:
            # Retrieve the prepared email object from DB
            email_obj = EmailMessage.objects.get(id=email_message_id)

            subject = email_obj.subject
            from_email = email_obj.from_email

            # Django email
            message = EmailMultiAlternatives(
                subject=subject,
                body=email_obj.body_text or "",
                from_email=from_email,
                to=[r.recipient_email for r in email_obj.recipients.filter(type="to")],
                cc=[r.recipient_email for r in email_obj.recipients.filter(type="cc")],
                bcc=[r.recipient_email for r in email_obj.recipients.filter(type="bcc")],
            )
            
            if email_obj.body_html:
                message.attach_alternative(email_obj.body_html, "text/html")
            
            for attachment in email_obj.attachments.all():
                message.attach(attachment.file_name, attachment.file.read(), attachment.mime_type)
            
            extra_headers = {}
            for header in email_obj.headers.all():
                extra_headers[header.header_name] = header.header_value
            if extra_headers:
                message.extra_headers = extra_headers
            
            message.send()

            # Update DB 
            email_obj.status = "sent"
            email_obj.sent_at = timezone.now()
            email_obj.save()

            return True

        except Exception as e:
            email_obj.status = "failed"
            email_obj.error_message = str(e)
            email_obj.retry_count += 1
            email_obj.save()
            return False

    @staticmethod
    def queue_template_email(subject, to, template_path, context, from_email=None, cc=None, bcc=None):
        # Render templates
        text = render_to_string(f"emails/{template_path}.txt", context)
        html = render_to_string(f"emails/{template_path}.html", context)

        # Create EmailMessage
        email_msg = EmailMessage.objects.create(
            subject=subject,
            from_email=from_email,
            body_text=text,
            body_html=html,
        )

        #Recipients
        for email in to:
            EmailRecipient.objects.create(email_message=email_msg, recipient_email=email, type="to")
        if cc:
            for email in cc:
                EmailRecipient.objects.create(email_message=email_msg, recipient_email=email, type="cc")
        if bcc:
            for email in bcc:
                EmailRecipient.objects.create(email_message=email_msg, recipient_email=email, type="bcc")

        return email_msg