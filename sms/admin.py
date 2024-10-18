from django.contrib import admin
from .models import OtpSmsToken

# Register your models here.
@admin.register(OtpSmsToken)

class PhoneOtpTokenAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'verified', 'timestamp', 'date_of_expiry', 'max_otp_tries')
    search_fields = ('mobile_number',)
    list_filter = ('verified', 'timestamp')