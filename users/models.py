from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('applicant', 'Applicant'),
        ('recruiter', 'Recruiter')
    )

    otp_verified = models.BooleanField(default=True)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES)
    #otp = models.CharField(max_length=6, null=True, blank=True)
    #otp_time_stamp = models.DateTimeField(null=True, blank=True)

class Applicant(models.Model):

    resume = models.FileField(null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Recruiter(models.Model):

    company = models.CharField(null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)