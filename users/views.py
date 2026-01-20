from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from .models import CustomUser, Applicant, Recruiter
from .utils import send_otp, generate_otp, verify_otp
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register_page(request):

    if request.user.is_authenticated:
        return redirect("/dashboard/")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            query = CustomUser.objects.filter(email = form.cleaned_data['email'])
        
            if query.exists():
                messages.error(request, message="Email already registered!")
        
            else:
                #otp = generate_otp()
                #status = send_otp(form.cleaned_data['email'], otp)            
                
                #if status == 1:
                user = CustomUser.objects.create_user(role = form.cleaned_data['role'],
                                                      email = form.cleaned_data['email'],
                                                      username=form.cleaned_data['email'],
                                                      password = form.cleaned_data['password'],
                                                      last_name = form.cleaned_data['last_name'],
                                                      first_name = form.cleaned_data['first_name'])
                user.save()

                if form.cleaned_data['role'] == "applicant":
                    Applicant.objects.create(
                        user = user
                    )
                else:
                    Recruiter.objects.create(
                        user = user
                    )
                    
                messages.success(request, message="User registered successfully!")
                #request.session['otp_email'] = form.cleaned_data['email']
                return redirect('/user/login')
                
                #else:
                #    messages.error(request, message="Failed to sent verification OTP!")
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

    if request.user.is_authenticated:
        return redirect("/dashboard/")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            query = CustomUser.objects.filter(email = form.cleaned_data['email'])

            if query.exists():
                user = authenticate(request, username = form.cleaned_data['email'], password = form.cleaned_data['password'])

                if user is not None:
                    messages.success(request, "User logged in successfully!")
                    login(request, user)
                    return redirect("/")
                
                else:
                    messages.error(request, "Incorrect pssword!")
            
            else:
                messages.error(request, "Email doesnot exists!")
    else:
        form = LoginForm()

    return render(request, "auth/login.html", { "form": form})


def logout_page(request):
    
    if request.user.is_authenticated:
        logout(request)
    
    return redirect('/')
