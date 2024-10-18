from django.urls import path
from sms import views

app_name = 'sms'
urlpatterns = [
    path('mobile-otp/', views.OtpSmsCreateView.as_view(), name='generate-mobile-otp'),
    path('verify-mobile-otp/', views.VerifyOTPView.as_view(), name='verify-mobile-otp')
]