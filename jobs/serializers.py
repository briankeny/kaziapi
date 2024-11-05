from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Job,Review,JobApplication,JobPost, UserJobPostInteraction

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

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewDetailedSerializer(serializers.ModelSerializer):
    reveiwer= UserSerializer()
    jobpost = JobPostSerializer()
    class Meta:
        model = Review
        fields = '__all__'

class JobApplicationDetailedSerializer(serializers.ModelSerializer):
    applicant = UserSerializer()
    jobpost=JobPostSerializer()

    class Meta:
        model = JobApplication
        fields = '__all__'

class UserJobPostInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobPostInteraction
        fields = ['jobpost', 'user']
        extra_kwargs = {
            'jobpost': {'required': True},
        }    

