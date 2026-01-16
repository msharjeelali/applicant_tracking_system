from .models import CustomUser
from .forms import RegisterForm
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .utils import send_otp, generate_otp, verify_otp

# Create your views here.
def register_page(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            query = CustomUser.objects.filter(email = form.cleaned_data['email'])
        
            if query.exists():
                messages.error(request, message="Email already registered!")
        
            else:
                otp = generate_otp()
                status = send_otp(form.cleaned_data['email'], otp)            
                
                if status == 1:
                    user = CustomUser.objects.create_user(otp = otp,
                                                          username=form.cleaned_data['email'],
                                                          role = "applicant",
                                                          email = form.cleaned_data['email'],
                                                          password = form.cleaned_data['password'],
                                                          last_name = form.cleaned_data['last_name'],
                                                          first_name = form.cleaned_data['first_name'],
                                                          otp_time_stamp = timezone.now())
                    user.save()
                    messages.success(request, message="Verfication OTP sent to your email!")
                    request.session['otp_email'] = form.cleaned_data['email']
                    return render(request, 'auth/verify.html')
                
                else:
                    messages.error(request, message="Failed to sent verification OTP!")
    else:
        form = RegisterForm() 

    return render(request, 'auth/register.html', {'form': form})


def verify_page(request):
    
    email = request.session.get('otp_email')
    
    if not email:
        return render(request, 'forbiden.html')

    if request.method == "POST":
        otp = request.POST.get('otp')
        user = CustomUser.objects.filter(email = email)
        
        if not user.exists():
            messages.error(request, "Email not registered!")
        
        elif not user.otp_verified:
            sent_otp = user.otp
            
            if not verify_otp(sent_otp, otp):
                messages.error(request, "Invalid otp!")
            
            elif not user.otp_time_stamp:
                messages.error(request, "Otp expired!")
                
            else:
                sent_time = user.otp_time_stamp
                now = timezone.now()
                diff = now - sent_time

                if diff.total_seconds > settings.OTP_EXPIRY:
                    messages.error(request, 'Otp expired!')

                else:
                    messages.success(request, 'Otp verified successfully!')
                    user.otp_verified = True
                    user.save()
                    return redirect("user/login")
        
        else:
            messages.info(request, "Email already verified!")

    return render(request, 'auth/verify.html')



def login_page(request):
    return HttpResponse("Login Page")