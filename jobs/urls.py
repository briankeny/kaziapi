from django.urls import path
from .views import (UserListCreate, UserDetail, CompanyListCreate, CompanyDetail, 
                    JobListCreate, JobDetail, ApplicationListCreate, ApplicationDetail, 
                    SkillListCreate, SkillDetail, JobSkillListCreate, JobSkillDetail,
                    SavedJobListCreate, SavedJobDetail, ReviewListCreate, ReviewDetail)

urlpatterns = [
   
    path('jobs/', JobListCreate.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetail.as_view(), name='job-detail'),

    path('applications/', ApplicationListCreate.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', ApplicationDetail.as_view(), name='application-detail'),

    path('skills/', SkillListCreate.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', SkillDetail.as_view(), name='skill-detail'),

    path('job-skills/', JobSkillListCreate.as_view(), name='jobskill-list-create'),
    path('job-skills/<int:pk>/', JobSkillDetail.as_view(), name='jobskill-detail'),

    path('saved-jobs/', SavedJobListCreate.as_view(), name='savedjob-list-create'),
    path('saved-jobs/<int:pk>/', SavedJobDetail.as_view(), name='savedjob-detail'),

    path('reviews/', ReviewListCreate.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
