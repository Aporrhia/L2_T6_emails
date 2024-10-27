from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from .models import UserProfile
from .utils import get_user_email_connection
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            profile, created = UserProfile.objects.get_or_create(user=user)
            email_password = form.cleaned_data.get('email_password')
            profile.email_password = email_password 
            profile.save()

            messages.success(request, "Registration successful!")
            login(request, user)
            return redirect('send_email')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print("Login successful!")
                return redirect('send_email')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def send_email(request):
    if request.method == 'POST':
        recipients = request.POST.get('recipient').split(',')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print(f"Recipients: {recipients}")

        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile does not exist. Please register again.")
            return redirect('register')

        user_email = request.user.email
        user_email_password = profile.email_password

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=user_email,
            to=[email.strip() for email in recipients]
        )

        email.connection = get_user_email_connection(user_email, user_email_password)
        
        try:
            email.send(fail_silently=False)
            messages.success(request, "Email sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send email: {str(e)}")
        
        return redirect('send_email')

    return render(request, 'accounts/send_email.html')

def error_404(request, exception):
    return render(request, 'accounts/404.html', status=404)

def error_500(request):
    return render(request, 'accounts/500.html', status=500)