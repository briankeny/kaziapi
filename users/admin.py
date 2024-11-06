from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserSkill,UserInfo,ProfileVisit,SearchAppearance

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('user_id','email','mobile_number', 'username','verification_badge','location','longitude','latitude', 'full_name', 'account_type', 'is_staff','date_updated')
    list_filter = ('account_type', 'is_staff', 'is_superuser', 'is_active','verification_badge')
    search_fields = ('email','user_id','mobile_number', 'username', 'full_name')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'bio', 'profile_picture', 'mobile_number', 'location','longitude','latitude')}),
        ('Account Info', {'fields': ('account_type','verification_badge',)}),
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

# Register the models with the admin site
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'title', 'start_date', 'end_date')
    search_fields = ('user__username', 'subject', 'title')
    list_filter = ('start_date', 'end_date')


class ProfileVisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'visitor', 'timestamp')
    search_fields = ('user__username', 'visitor__username')
    list_filter = ('timestamp',)

class SearchAppearanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'count')
    search_fields = ('user__username',)
    list_filter = ('count',)

class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill_name')
    search_fields = ('user__username', 'skill_name')

admin.site.register(UserSkill, UserSkillAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(ProfileVisit, ProfileVisitAdmin)
admin.site.register(SearchAppearance, SearchAppearanceAdmin)