from django.urls import path
from .  import views

urlpatterns = [
   
    path('jobs/', views.JobList.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', views.JobDetail.as_view(), name='job-detail'),

    path('job-post-create/', views.JobPostCreate.as_view(), name='job-post-create'),
    path('job-posts/', views.JobPostList.as_view(), name='job-posts-list'),
    path('job-post/<int:pk>/', views.JobPostDetail.as_view(), name='job-post-detail'),

    path('analytics/', views.AnalyticsList.as_view(), name='analytics-detail'),

    path('job-application-create/',views.JobApplicationCreate.as_view(), name='job-application-create'),
    path('job-applications/',views.JobApplicationList.as_view(), name='job-application-list'),
    path('job-applications-user/',views.JobApplicationUserList.as_view(), name='job-app-user-list'),
    path('job-application/<int:pk>/', views.JobApplicationDetail.as_view(), name='application-detail'),
     path('reviews/', views.ReviewList.as_view(), name='reviews-list'),
    path('reviews-create/', views.ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>/',views.ReviewDetail.as_view(), name='review-detail'),
]

