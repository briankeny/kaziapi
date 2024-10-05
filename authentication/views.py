from django.forms import ValidationError
from rest_framework import generics
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from .models import PasswordResetToken
from .serializers import (ResetPasswordSerializer, VerifyCodeSerializer,ChangePasswordSerializer)
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework import status
from authentication.signals import reset_password_token_created
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.hashers import check_password
import random 
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class CustomObtainAuthLogin(TokenObtainPairView):

    def post(self,request,*args, **kwargs):
        # Validate public service number and password
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('user_id',None)
        try:  
            psn = int(psn) 
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error':'no user found matching credentials'},status=status.HTTP_404_NOT_FOUND)
        except ValueError:
             return Response({'error':'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)

        data = self.get_tokens_for_user(user)
        return Response(data,status=status.HTTP_201_CREATED)
    
    
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get(self,request,*args, **kwargs):
        return Response({"error":"Not Supported"},status=status.HTTP_403_FORBIDDEN)
    def patch(self,request,*args, **kwargs):
        return Response({"error":"Not Supported"},status=status.HTTP_403_FORBIDDEN)
    def put(self,request,*args, **kwargs):
        return Response({"error":"Not Supported"},status=status.HTTP_403_FORBIDDEN)

# This class based view handles Sending Verification Code Or Token  For Accounts that have Forgotten Passwords
class CustomResetPasswordRequestToken(generics.UpdateAPIView):

    def put(self, request, *args, **kwargs):  
        return Response({'message': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):  
        return Response({'message': 'Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        email = request.data.get('user_id')  
        if not email:
            return Response({'error': 'User Identification is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:

            User = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'You are not authorized to perform this operation'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            # Hide Information About The Non-Existence of this user
            Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate the password reset token
        def codeGen():
         code = round((random.random()*1000000))
         return code
                
        reset_password_token = codeGen() 
        
        # Trigger the signal to send the password reset email
        reset_password_token_created.send(sender=self.__class__, instance=User, reset_password_token=reset_password_token)

        return Response({'success': 'Password Reset Code has been sent to your email.'}, status=status.HTTP_200_OK)

# This view handles verification of Password Reset Confirmation Code.
    
class VerifyCodeView(generics.UpdateAPIView):
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError) and 'user_id' in exc.detail:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        user_id = serializer.validated_data['user_id']
        
        try:
            User = User.objects.get(email=user_id) or None
            if User.user_id:
                password_reset_token = PasswordResetToken.objects.get(user_id=User.user_id)
            else:
                raise ValidationError
            
        except Exception as e:
            return Response({'message': 'Invalid Credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cd = str(code)
            is_code_valid = check_password(cd,password_reset_token.code)
        except Exception as e:
            pass
        if is_code_valid:
            return Response({'message': 'Verification Code is valid.'}, status=status.HTTP_200_OK)
        else:
             return Response({'message': 'Invalid Verification code.'}, status=status.HTTP_401_UNAUTHORIZED)


    def delete(self, request, *args, **kwargs):  
        return Response({'message': 'Method not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):  
        return Response({'message': 'Unauthorized'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):  
        return Response({'message': 'Unauthorized'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# This class based view handles Password Change Process For Accounts that have Forgotten Passwords using Verification Code Sent by the above view
class ResetUserPassword(generics.UpdateAPIView):
     permission_classes = [AllowAny]
     serializer_class = ResetPasswordSerializer

     def put(self, request, *args, **kwargs):  
        return Response({'message': 'Unauthorized'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

     def patch(self, request, *args, **kwargs):  
        return Response({'message': 'Unauthorized'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
   
     def delete(self, request, *args, **kwargs):  
        return Response({'message': 'Method not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

     def post(self, request, *args, **kwargs):   
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        #Get The Mandatory fields From the Validated Data 
        code = serializer.validated_data['code']
        user_id = serializer.validated_data['user_id']
        try:
            User = User.objects.get(email=user_id) or None
            if User.user_id:
                password_reset_token = PasswordResetToken.objects.get(user_id=User.user_id)
            else:
                raise ValidationError
            
        except PasswordResetToken.DoesNotExist:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Compare The code Provided With the one in the db if they match 
        try:
            cd = str(code)
            is_code_valid = check_password(cd,password_reset_token.code)
        except Exception as e:
            pass
        if is_code_valid:
            # Check if the correct code has not yet Expired then Proceed to change Password
            if is_code_valid and password_reset_token.date_of_expiry > timezone.now():
                try:
                    psn = request.data.pop('user_id')
                    User = User.objects.get(public_service_no=psn)
                    # Change the password
                    new_password = serializer.validated_data['new_password']
                    User.set_password(new_password)
                    User.save()    
                    return Response({'message': 'Password was changed successfully.'}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                 return Response({'message': 'Verification Code Has Expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
             return Response({'message': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)    

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
    