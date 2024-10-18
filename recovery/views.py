import random 
from django.forms import ValidationError
from rest_framework import generics
from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
from .models import PasswordResetToken
from users.models import User
from .serializers import (ResetPasswordSerializer, VerifyCodeSerializer)
from rest_framework import status
from recovery.signals import reset_password_token_created
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password

# This class based view handles Sending Verification Code Or Token
#  For Users that have Forgotten their Passwords
class CustomResetPasswordRequestToken(generics.CreateAPIView):
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
class VerifyCodeView(generics.CreateAPIView):
    serializer_class = VerifyCodeSerializer
    permission_classes = [AllowAny]

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError) and 'user_id' in exc.detail:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)

    def create(self, request, *args, **kwargs):
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

# This class based view handles Password Change Process For Accounts that have Forgotten Passwords using Verification Code Sent by the above view
class ResetUserPassword(generics.CreateAPIView):
     permission_classes = [AllowAny]
     serializer_class = ResetPasswordSerializer

     def post(self, request, *args, **kwargs):   
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        #Get The Mandatory fields From the Validated Data 
        code = serializer.validated_data['code']
        user_id = serializer.validated_data['user_id']
        try:
            user = User.objects.get(email=user_id) or None
            if user.user_id:
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
                    user = User.objects.get(public_service_no=psn)
                    # Change the password
                    new_password = serializer.validated_data['new_password']
                    user.set_password(new_password)
                    user.save()    
                    return Response({'message': 'Password was changed successfully.'}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                 return Response({'message': 'Verification Code Has Expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
             return Response({'message': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)    

