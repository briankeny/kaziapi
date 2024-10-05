from django.urls import path
from authentication import views
from rest_framework_simplejwt.views import (TokenRefreshView)
app_name = 'authentication'
urlpatterns = [
    # Authentication & password reset urls 
    path('login/', views.CustomObtainAuthLogin.as_view(), name='app-login'),
    path('logout/', views.Logout.as_view(), name='api-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', views.CustomResetPasswordRequestToken.as_view() , name='password_reset'),
    path('password-reset/verify-code/',views.VerifyCodeView.as_view(), name="password-reset-verify-code"),
    path('password-reset/confirm/', views.ResetUserPassword.as_view() , name='password_reset-confirm'),
]