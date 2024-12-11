from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_mail(email, user_name):
    subject = "Welcome to Seller Account"
    message = f"Hello {user_name}, \n\nWelcome to your seller account! We're excited to have you with us."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_otp_mail(email, otp):
    subject = "OTP Code"
    message = f"Your OTP code is {otp}."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, "cspc186@gmail.com", recipient_list)


def send_otp_to_mail(otp, user_email):
    html_message = render_to_string('register.html', {
        'username': "username",
        'otp': otp,
    })
    plain_message = strip_tags(html_message)
    subject = 'OTP for Verification'
    send_mail(
        subject,
        plain_message,
        'cspc186@gmail.com',
        [user_email],
        html_message=html_message
    )