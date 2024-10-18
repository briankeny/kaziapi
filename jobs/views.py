from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination
from .models import (Job,JobApplication,JobAdvert,SavedJobAdvert,Review)
from .serializers import (JobApplicationSerializer,JobSerializer,SavedJobSerializer,ReviewSerializer,JobAdvertSerializer)


# Create Job Views

class JobListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    

class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# Create Job Advert Views

class JobAdvertListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = JobAdvert.objects.all()
    serializer_class = JobAdvertSerializer
    

class JobAdvertDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobAdvert.objects.all()
    serializer_class = JobAdvertSerializer


# Job Application Views

class JobApplicationListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

class JobApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer



# Saved Job Advert Views

class SavedJobListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = SavedJobAdvert.objects.all()
    serializer_class = SavedJobSerializer

class SavedJobDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    queryset = SavedJobAdvert.objects.all()
    serializer_class = SavedJobSerializer


# Review Views

class ReviewListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer