from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_name = models.CharField(max_length=100, default=None ,unique=True,null=False)
    job_skills =  ArrayField(models.CharField(max_length=100), default=None , null=False)

    def __str__(self):
     return self.job_name
    
    def save(self, *args, **kwargs):
        # Convert job_name to lowercase before saving
        self.job_name = self.job_name.lower()
        super(Job, self).save(*args, **kwargs)


class JobPost(models.Model):
    EMPLOYMENT_CHOICES = (
        ('Full time', 'Full time'),
        ('Part time', 'Part time'),
        ('Contract', 'Contract'),
        ('One time', 'One time'),
    )
    
    EXPERIENCE_CHOICES = (
        ('Entry level', 'Entry Level'),
        ('Mid level', 'Mid level'),
        ('Senior', 'Senior'),
        ('None', 'None'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed','Closed')
    )

    post_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Job,on_delete=models.SET_DEFAULT,default=None,blank=True,null=True)
    title = models.CharField(max_length=255,null=False,default=None)
    job_picture = models.ImageField(upload_to='job_pictures', null=True, blank=True,max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=20,default='full time', choices=EMPLOYMENT_CHOICES)
    experience_level = models.CharField(max_length=20, default='None',choices=EXPERIENCE_CHOICES)
    salary_range = models.CharField(max_length=50, null=True, blank=True)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobpost_recruiter')
    impressions = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='open', choices=STATUS_CHOICES)
    deadline_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=3600))
    date_posted = models.DateTimeField(auto_now_add=True)
    is_read_only = models.BooleanField(default=False)
    longitude = models.FloatField(default=-1.21999)
    latitude = models.FloatField(default=38.00899)

    def increment_impressions(self):
        self.impressions += 1
        self.save(update_fields=['impressions'])
    
    def __str__(self):
        return self.title

class UserJobPostInteraction(models.Model):
    jobpost = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='job_interactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_job_interaction')

    class Meta:
        unique_together = ('jobpost', 'user')

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied','applied'),
        ('reviewed','reviewed'),
        ('accepted','accepted'),
        ('declined','declined')
    )

    jobpost = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='job_application')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applicant')
    score  = models.PositiveIntegerField(default=0,null=False)
    status = models.CharField(max_length=20, default='applied')
    approval_date = models.CharField( default=timezone.now())
    application_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.approval_date = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.applicant.full_name} applied to {self.jobpost.title}"

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    reveiwer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviewer')
    jobpost = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='user_post')
    rating = models.PositiveIntegerField(default=0,null=False,)
    review_text = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review by {self.reveiwer.full_name} for {self.reveiwer.full_name}"
