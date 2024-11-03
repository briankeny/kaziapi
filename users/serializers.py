from rest_framework import serializers
from .models import User,UserSkill
from django.contrib.auth.hashers import make_password
from .models import UserInfo, ProfileVisit,SearchAppearance

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

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = [ 'id','user', 'subject', 'title', 'description', 'start_date', 'end_date']

class ProfileVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileVisit
        fields = ['user', 'visitor', 'timestamp']


class SearchAppearanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchAppearance
        fields = ['user', 'count']