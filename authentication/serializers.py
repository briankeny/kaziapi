from rest_framework import serializers
from users.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model =  User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

