from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Job, SavedJobPost,Review,JobApplication,JobPost

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'

class JobPostWithOwnerSerializer(serializers.ModelSerializer):
    recruiter = UserSerializer()
    category = JobSerializer()
    class Meta:
        model = JobPost
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'

class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJobPost
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
