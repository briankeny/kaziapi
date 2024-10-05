from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import status
import os
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions, IsAdminUser   
from django.db import IntegrityError
from rest_framework.exceptions import UnsupportedMediaType
from django.forms import ValidationError


class UserListView(generics.ListAPIView):
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'pk'
    parser_classes = (MultiPartParser,)
    renderer_classes = [JSONRenderer]
    queryset = User.objects.all()
    pagination_class = None
   
    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            if not (user.is_superuser or user.is_staff):
                return Response({"detail": "You Are not Authorized to Perform This Operation"},
                                status=status.HTTP_403_FORBIDDEN)
            response = super().create(request, *args, **kwargs)
            return response
        except ValidationError as e: 
            return Response({'error':'Submit All Required Fields'},status=status.HTTP_400_BAD_REQUEST) 
        except ValueError as e:
            return Response({"error": "Submit Correct Data"},status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": "User With Matching Details Exists"},status=status.HTTP_400_BAD_REQUEST)
        except UnsupportedMediaType as e:
            return Response({"error": "This Media Type is Not Supported Use Form Data"},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)    
      
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
        if not (user.is_superuser or user.groups.filter(name='UserAdmin').exists()):
           queryset = queryset.filter(email = user.email) 
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
            if not (instance.email == user.email or user.is_superuser or user.groups.filter(name='UserAdmin').exists()): 
                return Response({"message": "You are not authorized to perform this operation"}, 
                                status=status.HTTP_403_FORBIDDEN)

            # Prevent User From Changing Some Fields Unless Authorized
            nonChangeableFields = ['role','email','role']
            changed_fields = []

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


            serializer = self.get_serializer(instance, data=request.data, partial=True)
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

