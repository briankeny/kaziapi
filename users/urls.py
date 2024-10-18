from django.urls import path
from users import views

app_name = 'users'
urlpatterns = [
    # Users endpoints
    path('profile/', views.UserListView.as_view(), name='single-user-data'),
    path('users/', views.UserListView.as_view(), name='users-list'),
    path('user-registration/', views.UserCreate.as_view(), name='create-user'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    # Users skill endpoints

    path('user-skills/', views.UserSkillListCreate.as_view(), name='user-skill-list-create'),
    path('user-skill/<int:pk>/',views.UserSkillDetail.as_view(), name='user-skill-detail')
]



















