from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserSkill

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email','mobile_number', 'username', 'full_name', 'account_type', 'is_staff', 'date_updated')
    list_filter = ('account_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email','mobile_number', 'username', 'full_name')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'bio', 'profile_picture', 'mobile_number', 'address')}),
        ('Account Info', {'fields': ('account_type',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_updated')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'password1', 'password2', 'account_type')}
        ),
    )
    ordering = ('email',)

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill_name')
    search_fields = ('skill_name', 'user__email')
