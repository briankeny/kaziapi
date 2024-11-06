import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.dispatch import receiver,Signal
from .models import Message,Chat

# VendorFillingStationSupplyReport Notification
@receiver(post_save, sender=Message)
def  update_Chat(sender, instance, created, **kwargs):
    if created:
        content=''

        if instance.media:
            formated = instance.media.split('messages_media/')[1]
            content+= formated + ':'+ ' '

        if instance.content:
            content += instance.content
        
        try:
            convo = Chat.objects.get(chat_id=instance.conversation.chat_id)
            if content:
                convo.latest_message  = content[:100]
                convo.save()
        except Exception as e:
            print(f'Error for chat signal {e}')
            pass