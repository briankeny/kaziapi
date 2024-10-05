from rest_framework import serializers
from .models import User,UserSkill
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  
    
    # Exclude password from serialization
    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)  # Hash the password
        validated_data['password'] = hashed_password
        return super().create(validated_data)    
    class Meta:
       
        model = User
        fields = '__all__'


class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'


