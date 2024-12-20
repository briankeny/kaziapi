from django.db import models
from users.models import User


# Create your models here.
class Notification(models.Model):
    NOTIFICATION_Categ_CHOICES = (
        ('general','general'),
        ('review', 'review'),
        ('jobapplication','jobapplication'),
        ('jobpost', 'jobpost'),
        ('user','user'),
        ('message','message')
    )

    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='target_user')
    message = models.TextField(blank=True)
    subject = models.CharField(max_length=150, default=None, null=True)
    action=models.CharField(max_length=100, default=None, null=True)
    read_status  = models.BooleanField(default=False)
    notification_category = models.CharField(
        max_length=100,
        choices=NOTIFICATION_Categ_CHOICES,
        default='message'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
      
    def __str__(self):
        return f'{self.notification_id} - {self.user.full_name} -{self.notification_category}'
