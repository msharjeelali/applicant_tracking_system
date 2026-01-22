from django.urls import path
from . import views

urlpatterns = [
    path('', views.jobs_page, name='jobs_page')
]