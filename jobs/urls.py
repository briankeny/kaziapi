from django.urls import path
from .  import views

urlpatterns = [
   
    path('jobs/', views.JobListCreate.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', views.JobDetail.as_view(), name='job-detail'),

    path('job-posts/', views.JobAdvertListCreate.as_view(), name='jobskill-list-create'),
    path('job-post/<int:pk>/', views.JobAdvertDetail.as_view(), name='jobskill-detail'),

    path('job-applications/',views.JobApplicationListCreate.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', views.JobApplicationDetail.as_view(), name='application-detail'),

    path('saved-jobs/', views.SavedJobListCreate.as_view(), name='savedjob-list-create'),
    path('saved-jobs/<int:pk>/', views.SavedJobDetail.as_view(), name='savedjob-detail'),

    path('reviews/', views.ReviewListCreate.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/',views.ReviewDetail.as_view(), name='review-detail'),
]
