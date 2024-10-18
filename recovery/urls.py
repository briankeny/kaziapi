from django.urls import path
from . import views

app_name = 'recovery'
urlpatterns = [
    path('password-reset/', views.CustomResetPasswordRequestToken.as_view() , name='password_reset'),
    path('password-reset/verify-code/',views.VerifyCodeView.as_view(), name="password-reset-verify-code"),
    path('password-reset/confirm/', views.ResetUserPassword.as_view() , name='password_reset-confirm'),
]