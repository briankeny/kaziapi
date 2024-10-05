# serializers.py
from rest_framework import serializers
from .models import  Message, Chat
from users.serializers import UserSerializer

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class ChatWithParticipantsSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    class Meta:
        model = Chat
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
