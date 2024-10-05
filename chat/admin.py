from django.contrib import admin
from .models import (Chat,Message)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass
