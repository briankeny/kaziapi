from rest_framework import serializers
from .models import PasswordResetToken
from rest_framework import serializers

class VerifyCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)
    class Meta:
        model = PasswordResetToken 
        fields = ['mobile_number','otp']


class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    class Meta:
        model = PasswordResetToken 
        fields = ['code', 'mobile_number', 'new_password']
