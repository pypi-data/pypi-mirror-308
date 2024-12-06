# We can use a package that actually generates an otp and has an expiration time 

import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings


def generateotp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])



def send_code_to_user(email):
    Subject = "One time passcode for Email verification"
    otp_code = generateotp()
    user = User.objects.get(email=email)
    current_site = "myAuth.com"
    email_body = f"Hi {user.first_name}, thanks for signing up on {current_site} please verify your email with the \n one time passcode {otp_code}"
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.update_or_create(user=user, defaults={"code": otp_code})

    send_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])

    send_email.send(fail_silently=True)


def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[data['to_email']]
    )
    email.send(fail_silently=True)


