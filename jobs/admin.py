from django.contrib import admin
from .models import Job, JobPost, JobApplication, SavedJobPost, Review

# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'job_name')  # Customize the columns displayed in the admin list view

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'title','job_picture', 'location', 'employment_type', 
                    'experience_level', 'salary_range', 'status', 'date_posted')
    list_filter = ('employment_type', 'experience_level', 'status')  # Filters on the right sidebar
    search_fields = ('title', 'location', 'recruiter__email')  # Search fields in admin

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('jobpost', 'applicant', 'score', 'status', 'application_date')
    list_filter = ('status',)
    search_fields = ('applicant__email', 'jobpost__title')

@admin.register(SavedJobPost)
class SavedJobAdvertAdmin(admin.ModelAdmin):
    list_display = ('save_id', 'user', 'savedjob', 'date_posted')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'reveiwer', 'rating', 'date_posted')
    list_filter = ('rating',)
    search_fields = ('reveiwer__email', 'User__email')
