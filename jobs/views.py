from django.db.models import F
from rest_framework import generics,permissions,status
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination
from .models import (Job,JobApplication,JobPost,Review, UserJobPostInteraction )
from .serializers import (JobApplicationSerializer,JobSerializer,ReviewSerializer,JobApplicationDetailedSerializer,
                          JobPostWithOwnerSerializer,JobPostSerializer, UserJobPostInteractionSerializer)
from rest_framework.response import Response
from users.models import ProfileVisit,SearchAppearance

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
        # Increment impressions for each post in the queryset
        queryset.update(impressions=F('impressions') + 1)
        return queryset
    
class JobPostDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

    def get(self, request, pk):
        job_post = JobPost.objects.get(pk=pk)
        # Increment impressions 
        job_post.increment_impressions()  
        serializer = JobPostWithOwnerSerializer(job_post)
        return Response(serializer.data)


# Job Application Create View
class JobApplicationCreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

# Job Application List 
class JobApplicationList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        queryset  = JobApplication.objects.all()
        # Optional search term filtering
        search_term = str(self.request.query_params.get('searchTerm', None))
        search = str(self.request.query_params.get('search', None))
            # Sort order based on newer ones        
        queryset = queryset.order_by('score')          

        if search_term != 'None' and search != 'None':
                try:
                    field = f'{search_term}__icontains'
                    # Using filter() for case-insensitive search using icontains
                    queryset = queryset.filter(**{field: search})
                except Exception as e:
                        queryset = []
        return queryset


# Job Application List 
class JobApplicationUserList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationDetailedSerializer

    def get_queryset(self):
        user = self.request.user
        queryset  = JobApplication.objects.all()
        # Optional search term filtering
        search_term = str(self.request.query_params.get('searchTerm', None))
        search = str(self.request.query_params.get('search', None))
            # Sort order based on newer ones        
        queryset = queryset.order_by('score')          

        if search_term != 'None' and search != 'None':
                try:
                    field = f'{search_term}__icontains'
                    # Using filter() for case-insensitive search using icontains
                    queryset = queryset.filter(**{field: search})
                except Exception as e:
                        queryset = []
        return queryset


# Job Application Detail
class JobApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer


    def delete(self, request, *args, **kwargs):
            user = self.request.user
            instance = self.get_object()
            if not( user.user_id  == instance.applicant.user_id):
               return Response({'message':'You are not allowed to perform this operation'},
                               status=status.HTTP_406_NOT_ACCEPTABLE)
            instance.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)


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

class AnalyticsList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    pagination_class = None
    queryset = JobPost.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        data = {}
        
        # Count Profile Visits and Searches
        visits_count = ProfileVisit.objects.filter(user=user).count()
        search_appearance = SearchAppearance.objects.filter(user=user).first()
        searches_count = search_appearance.count if search_appearance else 0

        data['profilevisits'] = visits_count
        data['searches'] = searches_count

        if user.account_type == 'recruiter':
            # Get Job Posts for Recruiter
            jobposts = JobPost.objects.filter(recruiter=user)
            open_posts = jobposts.filter(status='open').count()
            closed_posts = jobposts.count() - open_posts
            
            # Aggregate Impressions and Reviews
            total_impressions = 0
            total_reviews = 0

            for post in jobposts:
                total_impressions += post.impressions
                total_reviews += Review.objects.filter(jobpost=post).count()

            data.update({
                'reviews': total_reviews,
                'impressions': total_impressions,
                'open': open_posts,
                'closed': closed_posts,
                'posts': jobposts.count()
            })

        else:
            # Get Applications for Jobseeker
            applications = JobApplication.objects.filter(applicant=user)
            open_statuses = ['applied', 'reviewed']
            open_applications = applications.filter(status__in=open_statuses).count()
            closed_applications = applications.count() - open_applications

            # Count Reviews for Jobseeker
            reviews_count = Review.objects.filter(reviewer=user).count()
            impressions_count = reviews_count + applications.count()

            data.update({
                'reviews': reviews_count,
                'impressions': impressions_count,
                'open': open_applications,
                'closed': closed_applications,
                'posts': applications.count()
            })

        return Response(data, status=status.HTTP_200_OK)
    


class UserJobPostInteractionCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserJobPostInteraction.objects.all()
    serializer_class = UserJobPostInteractionSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = request.data.copy()
        data['user'] = user.user_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # Save the new interaction
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
