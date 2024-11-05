from django.db.models import F
from rest_framework import generics,permissions,status
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination
from .models import (Job,JobApplication,JobPost,Review, UserJobPostInteraction )
from .serializers import (JobApplicationSerializer,JobSerializer,ReviewSerializer,
                          ReviewDetailedSerializer,
                          JobApplicationDetailedSerializer,
                          JobPostWithOwnerSerializer,JobPostSerializer, UserJobPostInteractionSerializer)
from rest_framework.response import Response
from users.models import ProfileVisit,SearchAppearance
from rest_framework.parsers import MultiPartParser
from jobs.signals import close_job_post_applications

# Create Job Views
class JobList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
    def get_queryset(self):
        queryset = Job.objects.all()
        # Optional search term filtering
        search_term = str(self.request.query_params.get('searchTerm','empty'))
        search = str(self.request.query_params.get('search','empty'))

        if search_term != "empty" and search != "empty":
            try:
                field = f'{search_term}__icontains'
                # Use filter() for case-insensitive search using icontains
                queryset = queryset.filter(**{field: search})
            except Exception as e:
                queryset = []

        return queryset

class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# List Jobs Views
class JobPostCreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobPostSerializer
    parser_classes=(MultiPartParser,)

    def create(self, request, *args, **kwargs):
        user = self.request.user

        # Allow only recruiters to create posts
        if user.account_type != 'recruiter':
            return Response(
                {'error': 'You are not allowed to perform this operation'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        data['recruiter'] = user.user_id
        serializer = self.get_serializer(data=data, partial=True)

        # Check if serializer data is valid
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

        # Optional search term filtering
        recruiter = self.request.query_params.get('recruiter','empty')

        if recruiter != 'empty':
            try:
                id= int(recruiter)
                queryset= JobPost.objects.filter(recruiter=id)     
            except Exception as e:
                queryset = JobPost.objects.none()

        else:
            queryset = queryset.order_by('date_posted')          
            search_term = str(self.request.query_params.get('searchTerm', None))
            search = str(self.request.query_params.get('search', None))
            if search_term != 'None' and search != 'None':
                try:
                        field = f'{search_term}__icontains'
                        # Using filter() for case-insensitive search using icontains
                        queryset = queryset.filter(**{field: search})
                except Exception as e:
                        queryset = JobPost.objects.none()
            # Increment impressions for each post in the queryset
            queryset.update(impressions=F('impressions') + 1)
            # Sort order based on newer ones        
        return queryset
    
class JobPostDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

    # def get(self, request, pk):
    #     user=self.request.user
    #     job_post = self.get_object()
    #     # Increment impressions 
    #     if user.user_id != job_post.recruiter.user_id: 
    #         job_post.increment_impressions()  
    #     serializer = self.serializer_class(job_post)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
         user = self.request.user
         object = self.get_object()
         requestData = request.data.copy()
         poststatus = requestData.get('status',None)

         if object.is_read_only:
              return Response({'This Action is forbidden'},status=status.HTTP_403_FORBIDDEN)
         
         if user.account_type != 'recruiter' and user.user_id != object.recruiter.user_id:
              return Response({'This Action is not permitted'},status=status.HTTP_403_FORBIDDEN)
         
         if  poststatus != None and object.status != poststatus and poststatus == 'closed':
              requestData['is_read_only'] = True
              close_job_post_applications.send(sender=JobPost, instance=object)

         serializer = self.get_serializer(object, data=requestData, partial=True)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data,status=status.HTTP_200_OK)          
    

    def delete(self, request, *args, **kwargs):
         user = self.request.user
         object = self.get_object()
         if object.recruiter.user_id != user.user_id:
            return Response({'error':'You cannot perform this operation'},status=status.HTTP_403_FORBIDDEN)
         object.delete()
         return Response({},status=status.HTTP_204_NO_CONTENT)

# Job Application Create View
class JobApplicationCreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not user.account_type == 'jobseeker':
            return Response({'error':'You are not allowed to perform this operation'},status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

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
        # queryset = queryset.order_by('score')          

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
        applicant = self.request.query_params.get('applicant','empty')
        jobpost = self.request.query_params.get('jobpost','empty')

        if applicant != 'empty':
            try:
                id= int(applicant)
                queryset = JobApplication.objects.filter(applicant=id)
            except Exception as e:
                queryset=[]
            return queryset
        
        elif jobpost != 'empty':
            try:
                id= int(jobpost)
                queryset = JobApplication.objects.filter(jobpost=id)
            except Exception as e:
                queryset=[]
            return  queryset
        else:
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


    def patch(self, request, *args, **kwargs):
         user = self.request.user
         object = self.get_object()

         if user.account_type != 'recruiter' and user.user_id != object.jobpost.recruiter.user_id:
              return Response({'This Action is not permitted'},status=status.HTTP_403_FORBIDDEN)
         
         serializer = self.get_serializer(object, data=request.data, partial=True)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data,status=status.HTTP_200_OK)          
    

    def delete(self, request, *args, **kwargs):
            user = self.request.user
            instance = self.get_object()
            if not( user.user_id  == instance.applicant.user_id):
               return Response({'message':'You are not allowed to perform this operation'},
                               status=status.HTTP_406_NOT_ACCEPTABLE)
            instance.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)


# Review Views
class ReviewList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 
    queryset = Review.objects.all()
    serializer_class = ReviewDetailedSerializer


    def get_queryset(self):
        user = self.request.user
        queryset  = Review.objects.all()
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

# Review Views
class ReviewCreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        # Allow only recruiters to create posts
        if user.account_type == 'recruiter':
            return Response(
                {'error': 'You are not allowed to perform this operation'},
                status=status.HTTP_403_FORBIDDEN
            )
        data = request.data.copy()
        data['reveiwer'] = user.user_id
        serializer = self.get_serializer(data=data)
        # Check if serializer data is valid
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class AnalyticsList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    pagination_class = None
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        data = {}
        
        # Count Profile Visits and Searches
        visits_count = ProfileVisit.objects.filter(user=user.user_id).count()
        search_appearance = SearchAppearance.objects.filter(user=user.user_id).first()
        searches_count = search_appearance.count if search_appearance else 0

        data['profilevisits'] = visits_count
        data['searches'] = searches_count

        if user.account_type == 'recruiter':
            # Get Job Posts for Recruiter
            jobposts = JobPost.objects.filter(recruiter=user.user_id)
            open_posts = jobposts.filter(status='open').count()
            closed_posts = jobposts.count() - open_posts
            
            # Aggregate Impressions and Reviews
            total_impressions = 0
            total_reviews = 0

            for post in jobposts:
                total_impressions += post.impressions
                total_reviews += Review.objects.filter(jobpost=post.post_id).count()

            data.update({
                'reviews': total_reviews,
                'impressions': total_impressions,
                'open': open_posts,
                'closed': closed_posts,
                'posts': jobposts.count()
            })

        else:
            # Get Applications for Jobseeker
            applications = JobApplication.objects.filter(applicant=user.user_id)
            open_statuses = ['applied', 'reviewed']
            open_applications = applications.filter(status__in=open_statuses).count()
            closed_applications = applications.count() - open_applications

            # Count Reviews for Jobseeker
            reviews_count = Review.objects.filter(reveiwer=user.user_id).count()
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
