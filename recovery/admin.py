from django.contrib import admin
from .models import PasswordResetToken

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'code', 'date_of_creation', 'date_of_expiry')
    search_fields = ('user_id__username', 'code')
    list_filter = ('date_of_creation', 'date_of_expiry')
    ordering = ('-date_of_creation',)
