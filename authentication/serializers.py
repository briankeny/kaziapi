from rest_framework import serializers
from .models import( PasswordResetToken)
from rest_framework import serializers
from users.models import User
 

class VerifyCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True)
    class Meta:
        model = PasswordResetToken 
        fields = '__all__'


class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    class Meta:
        model = PasswordResetToken 
        fields = ['code', 'user_id', 'new_password']


class ChangePasswordSerializer(serializers.Serializer):
    model =  User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

