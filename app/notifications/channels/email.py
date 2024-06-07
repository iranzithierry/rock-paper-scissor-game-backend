from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from app.tasks import send_email_task


class EmailChannel:
    @staticmethod
    def send(context, html_template, subject, to):
        if isinstance(to, str):
            to = [to]

        email_html_message = render_to_string(html_template, context)

        send_email_task(subject, to, settings.EMAIL_FROM, email_html_message)
        return
