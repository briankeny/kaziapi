from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from users.models import User
from .models import Notification
from jobs.models import JobPost
from django.dispatch import receiver
from django.core.mail import send_mail  
from django.conf import settings

# Function for saving Notification
def save_Notification(subject="",message="",category="",receiver=None,action=None):
    try:
        if receiver:
            notification = Notification(
                subject = subject,
                message = message,
                notification_category = category,
                user = receiver,
                action=action,
                )
            notification.save()
    except Exception as e :
            print(f'Saving not error {e}')
            pass  


def send_notification_email(subject="",message="",recipients=[]):
    try:
        sender = settings.EMAIL_HOST_USER
        send_mail(subject,message,sender,recipients)
    except Exception as e:
         print(f'Found Email error {e}')
         pass


# Send a welcome Message To New Accounts
@receiver(post_save,sender =User)
def send_welcome_message(sender, instance, created, **kwargs):
    if created :
        notification_category = "general"
        # Notify Super User A New User Has Created An Account
        try:
            company = User.objects.get(is_superuser=True)
            action= f'/user/{company.user_id}/'
            #  Send Notification To The Organization
            message = f"{(instance.account_type).capitalize()}  {instance.full_name} username {instance.username}  has been registered successfuly!"
            subject = f"A New Account - {instance.full_name} Registration"
            save_Notification(subject,message,'user',company,f'/user/{instance.user_id}/')
        
        except User.DoesNotExist:
            company = None
            pass
                
        # Save Notification For New User
        message = "This organization is committed to serving you. Feel free to contact us for any inquiries or if you need assistance .Thank you for chosing us!"
        subject = f"{instance.full_name} welcome to KaziMtaani!"
        save_Notification(subject,message,notification_category,instance,action)

        if instance.email:
            send_notification_email(subject=subject,message=message,recipients=[instance.email])

# Job Post Notification
@receiver(post_save, sender=JobPost)
def send_Job_Post_notification(sender,instance,created,**kwargs): 
    if created:
        notification_category = "jobpost"
        action= f'/job-post/{instance.post_id}/'
        message = f"{instance.description[:200]}" 
        subject = f"New Job - {instance.title[:50]}"
        
        recipients = User.objects.filter(account_type='jobseeker')

        if len(recipients) >0 :
            for recipient in recipients:
                save_Notification(subject,message,notification_category,recipient,action)