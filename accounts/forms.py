from django import forms
from .models import User
from django.utils import timezone

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class OTPVerifyForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(max_length=6)

    def verify(self):
        from .models import EmailOTP, User
        email = self.cleaned_data['email']
        otp = self.cleaned_data['otp']
        otp_obj = EmailOTP.objects.filter(email=email, otp=otp).first()
        if not otp_obj or otp_obj.expires_at < timezone.now():
            raise forms.ValidationError("Invalid or expired OTP.")
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        otp_obj.delete()


class ResendOTPForm(forms.Form):
    email = forms.EmailField()
