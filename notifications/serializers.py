
from rest_framework import serializers
from .models import Notification
from users.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationDetailedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model=Notification
        fields = '__all__'
