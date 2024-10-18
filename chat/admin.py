from django.contrib import admin
from .models import Chat, Message

# Register the Chat model with customization
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'latest_message')
    search_fields = ('chat_id', 'participants__username')  # Allows searching by chat_id and participants
    filter_horizontal = ('participants',)  # Provides a better UI for managing ManyToMany fields

# Register the Message model with customization
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'conversation', 'sender', 'receiver', 'is_read', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')  # Search by sender, receiver, and message content
    list_filter = ('is_read', 'timestamp')  # Filter messages by whether they have been read or by the timestamp
    ordering = ('-timestamp',)  # Orders the messages by timestamp (latest first)

