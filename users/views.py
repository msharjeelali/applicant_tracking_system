from .models import CustomUser
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from .utils import send_otp, generate_otp

# Create your views here.
def register_page(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        last_name = request.POST.get("last-name")
        first_name = request.POST.get("first-name")
        re_password = request.POST.get("re-password")

        query = CustomUser.objects.filter(email = email)
        if query is None:
            messages.error(request, message="Email already registered!")
        
        elif password != re_password:
            messages.error(request, message="Passwords donot match!")

        else:
            otp = generate_otp()
            status = send_otp(email, otp)            
            if status == 1:
                user = CustomUser.objects.create_user(username=email,
                                                    otp = otp,
                                                    email = email,  
                                                    role = "applicant",
                                                    password = password, 
                                                    last_name = last_name, 
                                                    first_name = first_name, 
                                                    otp_time_stamp = timezone.now())
                user.save()
                messages.success(request, message="Verfication OTP sent to your email!")
            else:
                messages.error(request, message="Failed to sent verification OTP!")


    return render(request, 'auth/register.html')