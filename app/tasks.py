from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from app.celery import app


@shared_task()
def send_email_task(subject, to, default_from, email_html_message):
    msg = EmailMultiAlternatives(
        subject=subject,
        body=email_html_message,
        from_email=default_from,
        to=to,
        alternatives=((email_html_message, 'text/html'),),
    )
    msg.send()
