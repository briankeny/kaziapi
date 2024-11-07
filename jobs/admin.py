from django.contrib import admin
from .models import Job, JobPost, JobApplication, Review,UserJobPostInteraction

# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'job_name')  # Customize the columns displayed in the admin list view

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'title','job_picture', 'location', 'employment_type', 'longitude','latitude',
                    'experience_level', 'salary_range', 'status', 'date_posted')
    list_filter = ('employment_type', 'experience_level', 'status')  # Filters on the right sidebar
    search_fields = ('title', 'location', 'recruiter__full_name')  # Search fields in admin

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('jobpost', 'applicant', 'score', 'status', 'application_date')
    list_filter = ('status',)
    search_fields = ('applicant__email', 'jobpost__title')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'reveiwer', 'rating', 'date_posted')
    list_filter = ('rating',)
    search_fields = ('reveiwer__full_name', 'User__user_id')


# Optionally, create a custom admin class for additional customization
class UserJobPostInteractionAdmin(admin.ModelAdmin):
    list_display = ('jobpost', 'user')  # Display the job post and user in the list view
    list_filter = ('jobpost', 'user')   # Add filters for job posts and users
    search_fields = ('jobpost__title', 'user__full_name')  # Allow searching by job title and username

# Register the model and optional custom admin
admin.site.register(UserJobPostInteraction, UserJobPostInteractionAdmin)