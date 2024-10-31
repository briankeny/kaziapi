from rest_framework import generics,permissions
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination
from .models import (Job,JobApplication,JobPost,SavedJobPost,Review)
from .serializers import (JobApplicationSerializer,JobSerializer,SavedJobSerializer,ReviewSerializer,
                          JobPostWithOwnerSerializer,JobPostSerializer)


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

# List Jobs Views
class JobPostListCreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer


# Create Job Post Views
class JobPostList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = JobPost.objects.all()
    serializer_class = JobPostWithOwnerSerializer

    def get_queryset(self):
        user = self.request.user
        queryset  = JobPost.objects.all()

        if user.account_type == 'recruiter':
            queryset = JobPost.objects.filter(user=user)
        else:
            # Optional search term filtering
            search_term = str(self.request.query_params.get('searchTerm', None))
            search = str(self.request.query_params.get('search', None))
            # Sort order based on newer ones        
            queryset = queryset.order_by('date_posted')          
        
            if search_term != 'None' and search != 'None':
                try:
                    field = f'{search_term}__icontains'
                    # Using filter() for case-insensitive search using icontains
                    queryset = queryset.filter(**{field: search})
                except Exception as e:
                        queryset = []
        return queryset
    

class JobPostDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer


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
    queryset = SavedJobPost.objects.all()
    serializer_class = SavedJobSerializer

class SavedJobDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    queryset = SavedJobPost.objects.all()
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