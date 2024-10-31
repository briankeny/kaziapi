from django.urls import path
from .  import views

urlpatterns = [
   
    path('jobs/', views.JobListCreate.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', views.JobDetail.as_view(), name='job-detail'),

    path('job-post-create/', views.JobPostListCreate.as_view(), name='job-post-create'),
    path('job-posts/', views.JobPostList.as_view(), name='job-posts-list'),
    path('job-post/<int:pk>/', views.JobApplicationDetail.as_view(), name='job-post-detail'),

    path('job-applications/',views.JobApplicationListCreate.as_view(), name='application-list-create'),
    path('job-application/<int:pk>/', views.JobApplicationDetail.as_view(), name='application-detail'),

    path('saved-jobs/', views.SavedJobListCreate.as_view(), name='savedjob-list-create'),
    path('saved-job/<int:pk>/', views.SavedJobDetail.as_view(), name='savedjob-detail'),

    path('reviews/', views.ReviewListCreate.as_view(), name='review-list-create'),
    path('review/<int:pk>/',views.ReviewDetail.as_view(), name='review-detail'),
]
