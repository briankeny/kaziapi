import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from users.models import User
from .models import Notification
from django.dispatch import receiver,Signal
from django.core.mail import send_mail  

from django.contrib.auth.hashers import make_password

# Function for saving Notification
def save_Notification(title="",message="",type="message",category="detail_order",receiver=None,token=None,image=None,action=None):
    try:
        if receiver:
            notification = Notification(
                title = title,
                message = message,
                notification_type = type,
                notification_category = category,
                user = receiver,
                device_token = token,
                notification_image = image,
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



# Send Notification To Account
reset_password_token_created = Signal()
@receiver(reset_password_token_created)
def saveNotificationForPasswordResets(sender, instance, reset_password_token, *args, **kwargs):
    message = f'You Requested Verification Code That has been Sent to your Email Account. Regards @ICT Support Roads'
    title = "Password Reset"
    save_Notification(title=title,message=message,receiver=instance,image=instance.profile_picture)


# Send a welcome Message To New Accounts
@receiver(post_save,sender =User)
def send_welcome_message(sender, instance, created, **kwargs):
    if created :
        notification_type = "message"
        notification_category = "general"
        image = None
        action= instance.public_service_no
        
        try:
            ugc = User.objects.get(public_service_no=27000000000)
        except Exception as e:
            ugc = None
            pass
        
        if ugc != None:
            if instance.profile_picture:
                image = instance.profile_picture
            #  Send Notification To The Organization
            message = f"A New User {instance.first_name} {instance.last_name}. Public Service Number {instance.public_service_no}. Designation {instance.designation}, Has Been Registered Successfuly"
            title = f"Account {instance.first_name} {instance.last_name} Registration"
            save_Notification(title,message,notification_type,notification_category,ugc,None,instance.profile_picture,action)

        if str(instance.account_type).lower() != 'organization':
            if ugc !=  None:
                image = ugc.profile_picture
            # Save Notification For New User
            message = "Welcome To Roads Transport & Public Works, The County Government of Uasin Gishu. This Department is committed to serving the people of Uasin Gishu with Integrity and Excellence!. Feel Free to contact Us For Incquiries or if You Need Any Assistance .Thank You For Chosing Us!"
            title = f"{instance.first_name} Welcome To Roads Uasin Gishu County"
 
 # Detail Orders
@receiver(post_save, sender=DetailOrder)
def send_detail_Order_notification(sender,instance,created,**kwargs):
    notification_type = "message"
    notification_category = "detailorder"
    image = None
    action=instance.detail_order_no

    if created:  
        # Send Email Notification To Driver And Transport Managers
        notification_type = "message"
        image = instance.order_by.profile_picture
        admin_recipients=[]
        admins =[]
        ugc = None
        
        try:
            ugc = User.objects.get(public_service_no=2700000000000)
        except User.DoesNotExist:
            ugc =None
            pass

        # Notify User Detail Order Has Been Received             
        title= f'Your Order {instance.detail_order_no} Has Been Received!'
        # Save The Notification
        message = f'''Detail Order Reference Number {instance.detail_order_no} Has Been Received and is being processed at the moment. Please check notifications or track your order for updates on your order status.Regards @ICT Support Office Roads. Thank You!
        '''
        save_Notification(title,message,notification_type,notification_category,instance.order_by,None,image,action)
       
       
        if len(admin_recipients) > 0:
            if instance.order_by:
                    image = instance.order_by.profile_picture
            for recp in admin_recipients:
                # Notify Admins A New Order Has Been Posted
                title= f'New Fuel Order No: {instance.detail_order_no} was Posted!'
                message = f'''Detail Order Reference Number {instance.detail_order_no} Has been posted by {instance.order_by.first_name} {instance.order_by.last_name} Fuel Amount Requested is {instance.litres_fuel} litres {instance.fuel_type}.  Please click on learn more to view details.
                Regards @ICT Support Office Roads. Thank You!
                '''
                save_Notification(title,message,notification_type,notification_category,recp,None,image,action)
    else:
        if instance.order_status.lower() == 'confirmed':
            title= f'Order Ref No:{instance.detail_order_no} Confirmed!'
    
            if instance.authorized_by:
                image = instance.authorized_by.profile_picture

            check_Confirmation_Code(instance)
            code = generate_random_code()
            if code:
                tkn = str(code)
                hashed_Code = make_password(tkn)
                save_Confirmation_Code(instance,hashed_Code)
                
            # Send Email Notification To Driver
            if instance.order_by.email:    
                from_email = os.getenv('EMAIL_HOST_USER')
                recipient_list = [instance.order_by.email]
                subject = f'Detail Order {instance.detail_order_no} Confirmed!'
                message = f'''Your Detail Order Confirmation Code is: {code}. Use This Code To receive Fuel Dispensation At The Filling Station
                Regards @ICT Support Office Roads. Thank You!
                '''
                send_notification_email(from_email,subject,message,recipient_list) 

            # Save The Notification
            message = f'''Your Detail Order Reference Number {instance.detail_order_no} Has Been Confirmed! Confirmation Code is {code} You can Proceed To Fuel Your Vehicle. {instance.refill_instruction} Please Contact The Transport Officer For Further Instructions. 
            Regards @ICT Support Office Roads. Thank You!'''
            save_Notification(title,message,notification_type,notification_category,instance.order_by,None,image,action)
