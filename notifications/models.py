from django.db import models
from users.models import User

# Create your models here.

class Notification(models.Model):
    
    NOTIFICATION_Categ_CHOICES = (
        ('review', 'review'),
        ('jobadvert', 'jobadvert'),
        ('profile_visit','profile_visit'),
        ('new_message','new_message') 
    )

    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title  = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    subject = models.CharField(max_length=150, default=None, null=True)
    action=  models.CharField(max_length=100, default=None, null=True)
    delivery_status  = models.BooleanField(default=False)
    is_favourite = models.BooleanField(default=False)
    notification_image = models.ImageField(upload_to='profile_pictures', null=True, blank=True,max_length=300)
    notification_category = models.CharField(
        max_length=100,
        choices=NOTIFICATION_Categ_CHOICES,
        default='general'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
      
    def __str__(self):
        return f'{self.notification_id} - {self.user.first_name} -{self.notification_category}'
