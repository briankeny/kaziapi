from django.urls import path
from notifications import views

app_name = 'notifications'

urlpatterns = [
    path('notifications/', views.NotificationListView.as_view(), name='list-notifications'),
    path('notification/<int:pk>/', views.NotificationDetail.as_view(), name='update-notification'),
]







