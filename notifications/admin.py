from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'user','notification_category', 'read_status', 'timestamp')
    search_fields = ('user__username',  'subject', 'notification_category')
    list_filter = ('notification_category', 'read_status', 'timestamp')
    ordering = ('-timestamp',)

