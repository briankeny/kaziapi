from django.db import models
from .managers import UserManager
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser, PermissionsMixin):
    accounts = (('recruiter', 'recruiter'),('jobseeker', 'jobseeker'))
    BADGES = (
        # Reserved for companies and AI 
        ('tier_one','tier_one'), 
        # Reserved for verified recruiters
        ('tier_two','tier_two'),
        # Reserved for verified users
        ('tier_three','tier_three'),
        (None,None),
        )

    first_name=None
    last_name = None
    user_id = models.AutoField(primary_key=True)
    username= models.CharField(max_length=30, default=None,null=True,unique=True)
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
    industry = models.CharField(max_length=150,null=True,default=None)
    mobile_number = PhoneNumberField(null=False, blank=False, unique=True)
    mobile_verified = models.BooleanField(default=False,null=True)
    password = models.CharField(max_length=100, null=False,default=None)
    location = models.CharField(max_length=200, default="Eldoret", null=True)
    verification_badge = models.CharField(max_length=100, null=True,default=None,choices=BADGES)
    device_token = models.CharField(max_length=100,default=None, null=True,blank = True)
    date_updated = models.DateTimeField(default=timezone.now)
    longitude = models.FloatField(default=-1.21999)
    latitude = models.FloatField(default=38.00899)
   
    def __str__(self):
        return f"{self.user_id} - {self.full_name}"   

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.date_updated = timezone.now()
        super().save(*args, **kwargs)

   
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['full_name','account_type','email']

    def __str__(self):
        return f'{self.last_name}-{self.full_name}'
    

class UserSkill(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} - {self.skill_name}'


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_data')
    subject = models.CharField(max_length=100,null=False)
    title = models.CharField(max_length=255,null=False)
    description = models.TextField(default='',null=False)
    start_date =   models.DateTimeField(default=None,null=True)
    end_date =  models.DateTimeField(default=None,null=True)

    def __str__(self):
        return f'{self.user.full_name} {self.title}' 
    
class ProfileVisit(models.Model):
    id  = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    visitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_visitor')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
         # Ensures unique visits
        unique_together = ('user', 'visitor') 
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.full_name} visitor {self.visitor.full_name}'


class SearchAppearance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_appearances')
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.count} search appearances'