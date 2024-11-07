
from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [
    path('chats/', views.ChatList.as_view(), name='conversation-list'),
    path('chat/<int:pk>/', views.ChatDetail.as_view(), name='chat-details'),
    path('chat/<int:pk>/messages/', views.MessageList.as_view(), name='conversation-detail'),
    path('new-message/', views.MessageCreate.as_view(), name='message-create'),
    path('message/<int:pk>/', views.MessageDetail.as_view(), name='message-detail')
]





















