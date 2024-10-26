from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

def home(request):
    return render(request,'kaziweb/index.html',{'title':'Home Page'}) 

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'kaziweb/password-reset.html'  # Path to your custom template
    success_url = reverse_lazy('password_reset_complete')  # Redirect after success
