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
        mobi = request.data.get('mobile_number')  
        if not mobi:
            return Response({'error': 'User Identification is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            phone = str(mobi)
            user = User.objects.get(mobile_number=phone)
        except Exception as e:
            return Response({'error': 'You are not authorized to perform this operation'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate the password reset token
        def codeGen():
         code = round((random.random()*1000000))
         return code
                
        reset_password_token = codeGen() 

        # Trigger the signal to send the password reset email
        reset_password_token_created.send(sender=self.__class__, instance=user, reset_password_token=reset_password_token)
        return Response({'success': 'Password Reset Code has been sent to your phone number and email.'}, status=status.HTTP_200_OK)


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
        user_id = serializer.validated_data['mobile_number']
        
        try:
            user = User.objects.get(email=user_id) or None
            if user.user_id:
                password_reset_token = PasswordResetToken.objects.get(user_id=user.user_id)
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
        user_id = serializer.validated_data['mobile_number']
        try:
            user = User.objects.get(mobile_number=user_id) or None
            if user.user_id:
                password_reset_token = PasswordResetToken.objects.get(user_id=user.user_id)
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
        
        # Check if the correct code has not yet Expired then Proceed to change Password
        if is_code_valid and password_reset_token.date_of_expiry > timezone.now():
            # Change the password
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()    
            return Response({'message': 'Verification Code Has Expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
             return Response({'message': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)    