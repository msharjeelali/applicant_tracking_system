import random
from django.conf import settings
from django.core.mail import send_mail

def generate_otp():
    random.seed()
    otp = random.randint(100000, 999999)
    return otp

def verify_otp(otp, user_otp):
    return otp == user_otp

def send_otp(email, otp):
    subject = "Verify Your Identity"
    message = "Your verification code is " + str(otp) + ". Your code will expire in 5 minutes."
    return send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
