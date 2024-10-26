import os
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from users.models import User
from .models import (PasswordResetToken)
from django.dispatch import receiver,Signal
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail  
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Function For Sending Email Notifications
def send_email(subject, template, recipient_list, context):
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        html_message=html_message
    )


reset_password_token_created = Signal()
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        # Check if user already has a token
        token = PasswordResetToken.objects.get(user_id=instance.user_id)       
        # Remove existing token
        token.delete()
    except Exception as e:
        pass 

    # Create a new token
    unique_token =  create_Password_Reset_Token(instance, reset_password_token)
    subject = "Password Reset Request"
    template = "kaziweb/emailpassrecovery.html"
    recipient_list = [instance.email]
    
    link = f'{settings.API_DOMAIN}/password-reset/?token={unique_token}'
    context = {'full_name': instance.full_name, 'reset_link':link}

    # Send Password Reset Link To Email
    if instance.email_verified:
        send_email(subject, template, recipient_list, context)
           
def create_Password_Reset_Token(instance, reset_password_token):
    # Hash the token 
    tkn = str(reset_password_token)
    hashed_Code = make_password(tkn)
    try:
        User = User.objects.get(user_id=instance.user_id)
        # Create the PasswordResetToken instance
        passwordResetToken = PasswordResetToken(
            user_id=User,
            code=hashed_Code
        )
        passwordResetToken.save()
    except User.DoesNotExist:
        pass

    return hashed_Code


