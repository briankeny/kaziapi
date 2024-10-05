from django.db import models
from users.models import User


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    latest_message = models.CharField(max_length=250,blank=True,default='')

    def __str__(self):
        return f'{self.chat_id}'


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_receiver')
    content = models.TextField(default='',blank=True,null=True)
    media = models.FileField(upload_to='messages_media', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ID:{self.message_id} From - {self.sender.first_name} to {self.receiver.first_name} - chat - {self.conversation.chat_id} '
