from django.contrib import admin
from .models import (PasswordResetToken)


@admin.register(PasswordResetToken)
class PasswordAdmin(admin.ModelAdmin):
    pass

