from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class CustomObtainAuthLogin(TokenObtainPairView):
    def post(self,request,*args, **kwargs):
        # Validate public service number and password
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = request.data.get('mobile_number',None)
        try:  
            user = User.objects.get(mobile_number = uid)
        except User.DoesNotExist:
            return Response({'error':'User matching the given credentials does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({'error':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)

        data = self.get_tokens_for_user(user)
        return Response(data,status=status.HTTP_201_CREATED)
    
    
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get(self,request,*args, **kwargs):
        return Response({"error":"Not Supported"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self,request,*args, **kwargs):
        return Response({"error":"Not Supported"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def put(self,request,*args, **kwargs):
        return Response({"error":"Not Supported"},status=status.HTTP_405_METHOD_NOT_ALLOWED)

class Logout(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    
    def post(self,request,*args,**kwargs):
        user = self.request.user
        access = str(request.data.get('refresh',None))   
        # If user provided a key they want to blacklist 
        # Proceed to blacklist otherwise remove all sessions
        if access !=  'None':
            try:
                # Check If this Token is valid
                session_key = access
                ref_token = RefreshToken(session_key)
                ref_token.blacklist()
                return Response({'message':'Logout Success'},status=status.HTTP_200_OK)
         
            except Exception as e:
                return Response({'error':'You cannot perfom this  operation'},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'error':'Error Occurred During Logout'},status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,*args,**kwargs):
        return Response({'error':'Unsupported Request'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self,request,*args,**kwargs):
        return Response({'error':'Unsupported Request'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# This view handles changing Password For Already Authenticated Users.
class ChangePasswordView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):  
        return Response({'message': 'Method not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):  
        return Response({'message': 'Method not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"current_password": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password Was Updated successfully'
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
