from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_admission_email(subject, template_name, context, recipient_list):
    html_message = render_to_string(template_name, context)
    send_mail(
        subject=subject,
        message="",  # plain-text fallback left blank since we're sending HTML
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        html_message=html_message,
    )