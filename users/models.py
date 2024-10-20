from django.db import models
from .managers import UserManager
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser, PermissionsMixin):
    accounts = (('recruiter', 'recruiter'),('jobseeker', 'jobseeker'))
    first_name=None
    last_name = None
    user_id = models.AutoField(primary_key=True)
    username= models.CharField(max_length=30, default=None,null=False,unique=True)
    full_name = models.CharField(max_length=100, default=None, null=False,blank=True)
    bio = models.CharField(max_length=300, default="Hi there I'm on Kazi Mtaani",null=True,blank=True)
    email = models.CharField(max_length=100, default=None, null=True,unique=True)
    email_verified = models.BooleanField(default=False,null=True,blank=False)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True,max_length=300)
    account_type = models.CharField(  
        max_length=30,
        null=True,
        choices=accounts,
        default='jobseeker')
    mobile_number = PhoneNumberField(null=False, blank=False, unique=True)
    mobile_verified = models.BooleanField(default=False,null=True)
    password = models.CharField(max_length=100, null=False,default=None)
    address = models.CharField(max_length=200, default="Eldoret", null=True)
    device_token = models.CharField(max_length=100,default=None, null=True,blank = True)
    date_updated = models.DateTimeField(default=timezone.now)
   
    def __str__(self):
        return f"{self.user_id} - {self.first_name} {self.last_name}"   

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.date_updated = timezone.now()
        super().save(*args, **kwargs)

   
    REQUIRED_FIELDS = ['first_name','last_name','email','account_type']

    def __str__(self):
        return f'{self.last_name}-{self.first_name}'
    


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=255)

    def __str__(self):
        return self.skill_name