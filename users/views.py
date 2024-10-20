import os
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .models import User,UserSkill
from .serializers import UserSerializer,UserSkillSerializer
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError
from rest_framework.exceptions import UnsupportedMediaType
from django.forms import ValidationError
from sms.models import OtpSmsToken
from django.contrib.auth.hashers import check_password

class UserProfileView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    renderer_classes = [JSONRenderer]
    queryset = User.objects.all()
    pagination_class = None
    
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(email=user.email)
    
class UserCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = None
   
    def create(self, request, *args, **kwargs):
            # Copy request data
            data = request.data.copy()

            # Get Phone number from the request body 
            phone = request.data.get('mobile_number',None)
            otp = request.data.get('otp',None)
            user_name = request.data.get('username',None)
    
            if phone == None or otp == None or user_name == None:
                return Response({'error':'Missing Credentials'},status=status.HTTP_400_BAD_REQUEST)
            
            #Serialize the data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
    
            # Check if a user has this phone number
            try:
                usr = User.objects.get(mobile_number = phone)
                if usr:
                    return Response({'error':'An Account with this number already exists'},
                                    status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                pass

            # Check if user verified their phone number
            try:
                verified_number = OtpSmsToken.objects.get(mobile_number=phone)
                if verified_number.verified:
                    otp = str(otp)
                    is_code_valid = check_password(otp,verified_number.otp)
                    if not is_code_valid:
                        return Response({'error':'Phone number verification is required'},status=status.HTTP_400_BAD_REQUEST)
                    pass
                else:
                    return Response({'error':'Phone number verification is required'},status=status.HTTP_400_BAD_REQUEST)
                                
            except OtpSmsToken.DoesNotExist:
                return Response({'error':'Phone number verification is required'},status=status.HTTP_400_BAD_REQUEST)
            
            
            # Proceed to create the user
            serializer.validated_data['mobile_verified'] = True
            self.perform_create(serializer)  
            return Response({'message':'Your account has been created successfully!'},status=status.HTTP_201_CREATED)
     
class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'pk'
    renderer_classes = [JSONRenderer]
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination  # Set the pagination class

    def get_queryset(self):
        queryset = super().get_queryset()
        # Optional search term filtering
        ordering = str(self.request.query_params.get('ordering', 'email'))
        search_term = str(self.request.query_params.get('searchTerm','empty'))
        search = str(self.request.query_params.get('search','empty'))
        queryset = User.objects.all()
        if search_term != "empty" and search != "empty":
            try:
                field = f'{search_term}__icontains'
                # Use filter() for case-insensitive search using icontains
                queryset = queryset.filter(**{field: search})
            except Exception as e:
                queryset = User.objects.none()

        if ordering:
            try:
                queryset = queryset.order_by(ordering)
            except Exception as e:
                queryset = User.objects.none()

        return queryset

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes=(MultiPartParser,)
    lookup_field = 'pk'
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all() 
        queryset = queryset.filter(user_id = user.user_id) 
        
        return queryset
     
    def put(self, request, *args, **kwargs):
        return Response({"message":"Unsupported Request or Method not Allowed"},
                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    def patch(self, request, *args, **kwargs):
        try:
            # Get the person making the request from the request body
            user = self.request.user
            # Get the person referred to in this instance
            instance = self.get_object()       
            profile_picture = request.data.get('profile_picture', 'empty')
            requestData = request.data.copy()
        
            # Check if it is the same person or an authorized party, then proceed to make changes
            if not (instance.email == user.email): 
                return Response({"message": "You are not authorized to perform this operation"}, 
                                status=status.HTTP_403_FORBIDDEN)

            # Prevent User From Changing Some Fields Unless Authorized
            nonChangeableFields = ['role','email','role']

            # User id not authorized to change non changeable fields so we remove them from request.data
            requestData = {key: value for key, value in requestData.items() if key not in nonChangeableFields}  
            
            # User  Changing The Profile Picture
            if profile_picture != 'empty':
                # Delete the existing profile_picture if it exists
                existing_profile_picture = instance.profile_picture
                if existing_profile_picture:
                    path_to_existing_picture = os.path.join('media', str(existing_profile_picture))
                    if os.path.exists(path_to_existing_picture):
                        try:
                            os.remove(path_to_existing_picture)
                        except Exception as e:      
                            pass


            serializer = self.get_serializer(instance, data=requestData, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ValidationError as e: 
            return Response({'error':'Submit All Required Fields'},status=status.HTTP_400_BAD_REQUEST) 
        except ValueError as e:
            # Issue with data types
            return Response({"error": "Submit Correct Data"},status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            # Issue with constraint could be unique keys
            return Response({"error": "User With Matching Details Exists"},status=status.HTTP_400_BAD_REQUEST)
        except UnsupportedMediaType as e:
            return Response({"error": "This Media Type is not supported"},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)    
      
    # Attepting Delete
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({'message': 'You are not allowed to perform this operation'}, status=status.HTTP_403_FORBIDDEN)
        # Get the object to be deleted
        instance = self.get_object()
        # Perform the deletion
        instance.delete()
              
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    

class UserSkillListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer

class UserSkillDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
