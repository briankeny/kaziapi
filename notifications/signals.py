from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from users.models import User
from .models import Notification
from jobs.models import JobPost
from django.dispatch import receiver

# Function for saving Notification
def save_Notification(title="",message="",category="",receiver=None,participant=None,action=None):
    try:
        if receiver:
            notification = Notification(
                title = title,
                message = message,
                notification_category = category,
                user = receiver,
                participant = participant,
                action=action,
                )
            notification.save()
    except Exception as e :
            pass  


def send_notification_email(sender=None,subject="",message="",recipients=[]):
    try:
        pass
        #send_mail(subject,message,sender,recipients)
    except Exception as e:
         pass


# Send a welcome Message To New Accounts
@receiver(post_save,sender =User)
def send_welcome_message(sender, instance, created, **kwargs):
    if created :
        notification_type = "message"
        notification_category = "general"
        action= f'{instance.user_id}'
        participant = instance
    
        # Notify Super User A New User Has Created An Account
        try:
            company = User.objects.get(is_superuser=True)
        except Exception as e:
            company = None
            pass
        
        if company != None:
            #  Send Notification To The Organization
            message = f"{(instance.account_type).capitalize()}  {instance.full_name} username {instance.username}  Has Been Registered Successfuly"
            title = f"A New Account - {instance.full_name} Registration"
            save_Notification(title,message,notification_type,notification_category,company,[participant],action)

        # Send Welcome Message To The User
            if company != None and company.profile_picture:
                action = company
                participant = company
                
            # Save Notification For New User
            message = "Welcome To KaziMtaani. This Organization is committed to serving you. Feel Free to contact Us for any incquiries or if you need our assistance .Thank You For Chosing Us!"
            title = f"{instance.full_name} welcome to Kazi Mtaani"
            save_Notification(title,message,notification_type,notification_category,instance,[company],action)

 
# Job Posts
@receiver(post_save, sender=JobPost)
def send_JobPost_notification(sender,instance,created,**kwargs):
    notification_type = "message"
    notification_category = "jobpost"
    action=instance.post_id
    recipients = []

    # 
    if created:  
        # Notify People Subscribed to Owners Post:
        # try:
        #     users = User.objects.filter()
        # except Exception as e:
        #     pass

        pass

       
    