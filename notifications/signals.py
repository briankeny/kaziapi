from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from users.models import User
from .models import Notification
from jobs.models import JobPost,JobApplication,Review
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
            company = User.objects.filter(is_superuser=True).first()
            if company:
                action= f'{company.user_id}'
                #  Send Notification To The Organization
                message = f"{(instance.account_type).capitalize()}  {instance.full_name} username {instance.username}  has been registered successfuly!"
                subject = f"{instance.full_name} joined Kazi Mtaani!"
                save_Notification(subject,message,'user',company,f'{instance.user_id}')
        
        except User.DoesNotExist:
            company = None
            pass
                
        # Save Notification For New User
        message = "This organization is committed to serving you. Thank you for chosing us!"
        subject = f"{instance.full_name} welcome to KaziMtaani!"
        save_Notification(subject,message,notification_category,instance,action)

        if instance.email:
            send_notification_email(subject=subject,message=message,recipients=[instance.email])

# Job Post Notification
@receiver(post_save, sender=JobPost)
def send_Job_Post_notification(sender,instance,created,**kwargs): 
    if created:
        try:
            notification_category = "jobpost"
            action= f'{instance.post_id}'
            message = f"{instance.description[:200]}" 
            subject = f"New Job - {instance.title[:50]}"
            
            recipients = User.objects.filter(account_type='jobseeker')

            if len(recipients) >0 :
                for recipient in recipients:
                    if instance.category:
                        job_name = instance.category.job_name
                        if str(recipient.industry).lower() in  str(job_name).lower():
                            save_Notification(subject,message,notification_category,recipient,action)
        except Exception as e:
            pass


# Job Application Notification
@receiver(post_save, sender=JobApplication)
def send_Job_Application_notification(sender,instance,created,**kwargs): 
    if created:
        try:
            notification_category = "user"
            action= f'{instance.applicant.user_id}'
            message = f"{instance.applicant.bio[:100]}" 
            subject = f"{instance.applicant.full_name} applied for - {instance.jobpost.title}"
            
            recipient = instance.jobpost.recruiter
            save_Notification(subject,message,notification_category,recipient,action)
        except Exception as e:
            pass


# Job Review Notification
@receiver(post_save, sender=Review)
def send_Review_notification(sender,instance,created,**kwargs): 
    if created:
        try:
            notification_category = "user"
            action= f'{instance.reveiwer.user_id}'
            message = f"{instance.review_text[:200]}" 
            subject = f"{instance.reveiwer.full_name} reviewed - {instance.jobpost.title}"
            recipient = instance.jobpost.recruiter
    
            save_Notification(subject,message,notification_category,recipient,action)
        except Exception as e:
            pass