from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, EmailOTP
from .forms import RegisterForm, OTPVerifyForm, ResendOTPForm
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# REGISTER VIEW
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "OTP sent to email.")
            return redirect('verify-otp')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# VERIFY OTP VIEW
def verify_otp_view(request):
    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            form.verify()
            messages.success(request, "Email verified successfully.")
            return redirect('login')
    else:
        form = OTPVerifyForm()
    return render(request, 'accounts/verify_otp.html', {'form': form})


# RESEND OTP VIEW
def resend_otp_view(request):
    if request.method == 'POST':
        form = ResendOTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            if user.is_verified:
                messages.warning(request, "User already verified.")
                return redirect('login')

            EmailOTP.objects.filter(email=email).delete()

            otp = get_random_string(6, allowed_chars='0123456789')
            expires_at = timezone.now() + timedelta(minutes=5)

            EmailOTP.objects.create(email=email, otp=otp, expires_at=expires_at)
            send_mail(
                subject="Your OTP Code (Resent)",
                message=f"Your new OTP is {otp}",
                from_email=None,
                recipient_list=[email],
            )

            messages.success(request, "OTP resent successfully.")
            return redirect('verify-otp')
    else:
        form = ResendOTPForm()
    return render(request, 'accounts/resend_otp.html', {'form': form})


# USER PROFILE VIEW
@login_required
def user_profile_view(request, user_id):
    user_to_view = get_object_or_404(User, id=user_id)

    if request.user != user_to_view and not request.user.is_app_admin:
        messages.error(request, "You do not have permission to view this profile.")
        return redirect('user-profile', user_id=request.user.id)

    return render(request, 'accounts/user_profile.html', {'user': user_to_view})


# ADMIN USER LIST VIEW
@login_required
def user_list_view(request):
    if request.user.is_app_admin:
        users = User.objects.all()
        return render(request, 'accounts/all_users.html', {'users': users})
    else:
        messages.error(request, "Only admins can view all users.")
        return redirect('user-profile', user_id=request.user.id)
