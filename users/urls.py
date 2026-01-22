from django.urls import path
from . import views


urlpatterns = [
    #path('verify/', views.verify_page, name='verify_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('register/', views.register_page, name='register_page'),
]