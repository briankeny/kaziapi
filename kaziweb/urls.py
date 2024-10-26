from django.urls import path
from kaziweb import views

app_name = 'kaziweb'

urlpatterns = [
    path('', views.home, name='kaziMtaani-home'),
    path('reset-password/<token>/', views.PasswordResetConfirmView.as_view(), name='update-notification'),
]

