from django.contrib import admin
from .models import Job, JobAdvert, JobApplication, SavedJobAdvert, Review

# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'job_name')  # Customize the columns displayed in the admin list view

@admin.register(JobAdvert)
class JobAdvertAdmin(admin.ModelAdmin):
    list_display = ('advert_id', 'title', 'location', 'employment_type', 'experience_level', 'salary_range', 'status', 'date_posted')
    list_filter = ('employment_type', 'experience_level', 'status')  # Filters on the right sidebar
    search_fields = ('title', 'location', 'recruiter__email')  # Search fields in admin

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('jobadvert', 'applicant', 'score', 'status', 'application_date')
    list_filter = ('status',)
    search_fields = ('applicant__email', 'jobadvert__title')

@admin.register(SavedJobAdvert)
class SavedJobAdvertAdmin(admin.ModelAdmin):
    list_display = ('save_id', 'user', 'savedjob', 'date_posted')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'reveiwer', 'rating', 'date_posted')
    list_filter = ('rating',)
    search_fields = ('reveiwer__email', 'User__email')
