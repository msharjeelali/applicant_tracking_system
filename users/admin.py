from . import models
from django.contrib import admin

# Register your models here.

class CustomUserAdminModel(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name")

admin.site.register(models.Recruiter)
admin.site.register(models.Applicant)
admin.site.register(models.CustomUser, CustomUserAdminModel)