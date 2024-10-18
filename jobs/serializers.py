from rest_framework import serializers
from .models import Job, SavedJobAdvert,Review,JobApplication,JobAdvert

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobAdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAdvert
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'

class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJobAdvert
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
