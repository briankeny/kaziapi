import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from users.models import User
from .models import (PasswordResetToken)
from django.dispatch import receiver,Signal
from django.core.mail import send_mail  
from django.contrib.auth.hashers import make_password

# A function For Sending Emails 
def send_notification_email(sender=None,subject="",message="",recipients=[]):
    try:
        if len(recipients) >0 and sender is not None:
          send_mail(subject,message,sender,recipients)
    except Exception as e:
         pass

reset_password_token_created = Signal()
# Send Password Reset Token
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        # Check if user already has a token
        token = PasswordResetToken.objects.get(user_id=instance.username)       
        # Remove existing token
        token.delete()
    except Exception as e:
        pass 

    # Create a new token
    create_Password_Reset_Token(instance, reset_password_token)

    # Send email with the token
    subject = 'Password Reset Token'
    message = f'Your Password Reset Verification Code is: {reset_password_token}'
    from_email = os.environ.get('EMAIL_HOST')
    recipient_list = [instance.email]
    send_notification_email(subject, message, from_email, recipient_list)
              
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

# Remove Token if user had An Existing Token
@receiver(pre_save, sender=PasswordResetToken)
def remove_passwordResetToken(sender, instance, **kwargs):
    if instance.user_id:
        try:
            token = PasswordResetToken.objects.get(user_id=instance.user_id)
            token.delete()
        except PasswordResetToken.DoesNotExist:
            pass