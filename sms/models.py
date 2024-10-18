from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField    
    
# Create your models here.

class OtpSmsToken(models.Model):
    mobile_number = PhoneNumberField(null=False, blank=False, unique=True)
    otp = models.CharField(max_length=100, default=None, null=True)
    verified = models.BooleanField(default=False,null=True)
    max_otp_tries = models.PositiveIntegerField(default=2,null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    otp_try_date = models.DateTimeField(default=timezone.now)
    date_of_expiry = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=20))

    def save(self, *args, **kwargs):
        self.date_of_expiry = timezone.now() + timezone.timedelta(minutes=20)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.mobile_number}'