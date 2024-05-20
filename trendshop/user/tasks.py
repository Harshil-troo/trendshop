from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from trendshop.settings import EMAIL_HOST_USER


@shared_task()
def send_welcome_email(user_email, first_name):
    context = {'first_name': first_name}
    email_html = render_to_string('email/welcome_email.html', context)

    email = EmailMessage(
        subject='Welcome to You & Me Shop - Your Ultimate Shopping Destination!',
        body=email_html,
        from_email=EMAIL_HOST_USER,
        to=[user_email],
        headers={'Reply-To': EMAIL_HOST_USER}
    )
    email.content_subtype = "html"
    email.send(fail_silently=True)
