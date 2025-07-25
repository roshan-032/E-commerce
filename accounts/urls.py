from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify-otp'),
    path('resend-otp/', views.resend_otp_view, name='resend-otp'),
    path('user/<int:user_id>/', views.user_profile_view, name='user-profile'),
    path('users/', views.user_list_view, name='user-list'),
]
