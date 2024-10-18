from django.db import models
from django.utils import timezone
from users.models import User
    
class PasswordResetToken(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, default=None, null=True)
    date_of_creation = models.DateTimeField(default=timezone.now)
    date_of_expiry = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=20))

    def save(self, *args, **kwargs):
        self.date_of_expiry = timezone.now() + timezone.timedelta(minutes=20)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_id.username}'