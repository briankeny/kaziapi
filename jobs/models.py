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


class JobAdvert(models.Model):
    EMPLOYMENT_CHOICES = (
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
    )
    
    EXPERIENCE_CHOICES = (
        ('entry_level', 'Entry Level'),
        ('mid_level', 'Mid Level'),
        ('senior', 'Senior'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed','Closed')
    )

    advert_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,null=False,default=None)
    description = models.TextField()
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    salary_range = models.CharField(max_length=50, null=True, blank=True)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_by')
    status = models.CharField(max_length=20, default='open', choices=STATUS_CHOICES)

    deadline_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=3600))
    date_posted = models.DateTimeField(auto_now_add=True)
 
    def save(self, *args, **kwargs):
        self.date_of_expiry = timezone.now() + timezone.timedelta(minutes=20)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied','applied'),
        ('reviewed')
    )

    jobadvert = models.ForeignKey(JobAdvert, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    score  = models.PositiveIntegerField(default=0,null=False)
    status = models.CharField(max_length=20, default='applied')
    application_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.applicant.email} applied to {self.job.title}"

class SavedJobAdvert(models.Model):
    save_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    savedjob = models.ForeignKey(JobAdvert, on_delete=models.CASCADE, related_name='saved_by')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} saved {self.savedjob.title}"

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    reveiwer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviewer')
    jobadvert = models.ForeignKey(JobAdvert, on_delete=models.CASCADE, related_name='user_post')
    rating = models.IntegerField()
    review_text = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review by {self.reveiwer.full_name} for {self.reveiwer.full_name}"