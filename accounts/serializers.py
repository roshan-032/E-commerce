from rest_framework import serializers
from .models import User, EmailOTP
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.db import transaction

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        otp = get_random_string(6, allowed_chars='0123456789')
        expires_at = timezone.now() + timedelta(minutes=5)

        try:
            with transaction.atomic():
                # Create inactive user
                user = User.objects.create_user(**validated_data, is_active=False)

                # Create OTP
                EmailOTP.objects.create(email=email, otp=otp, expires_at=expires_at)

                # Send OTP email
                send_mail(
                    subject="Verify Your Email",
                    message=f"Your OTP is {otp}",
                    from_email=None,
                    recipient_list=[email],
                )

        except Exception as e:
            raise serializers.ValidationError("Registration failed: " + str(e))

        return user

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            record = EmailOTP.objects.get(email=data['email'], otp=data['otp'])
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

        if record.is_expired():
            raise serializers.ValidationError("OTP has expired.")

        user = User.objects.get(email=data['email'])
        user.is_verified = True
        user.is_active = True
        user.save()

        record.delete()  # Optional: cleanup

        return data



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone']  # Only these for normal user


class UserSerializer(serializers.ModelSerializer):  # Optional, for admin/full access
    class Meta:
        model = User
        fields = '__all__'
