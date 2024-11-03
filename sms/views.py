import random

from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.contrib.auth.hashers import check_password,make_password
from django.utils import timezone

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import OtpSmsToken
from .serializers import OtpSmsTokenSerializer,USSDRequestSerializer
from .talk import SMS
from users.models import User
from .ussd import KaziUSSDActions


#Create Phone OTP using POST method and Push OTP Code to mobile using Africastalking API sms service  
class OtpSmsCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OtpSmsTokenSerializer
    model = OtpSmsToken
   
    def create(self,request,*args,**kwargs):
        data = self.request.data.copy()
        phone = data.get('mobile_number',None)        
        
        if phone ==None :
            return Response({'error':'Phone number is required'},status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a 6 digit code        
        def codeGen():
            code = round((random.random()*1000000))
            return code

        tkn = codeGen()
        tkn_str =str(tkn)
        token= make_password(tkn_str)

        print(f'OTP Code is {tkn}')

        # send the code
        message = f'Dear Customer your OTP is {tkn}. Use this code to verify your account with Kazi Mtaani'
        convo = SMS( recipients=[phone], message = message)
       
        # Check if the User has tried recently
        try:
             existing_token = OtpSmsToken.objects.get(mobile_number=phone)
             user_max_tries = existing_token.max_otp_tries <= 0 
             #existing_token.otp_try_date is existing_token.timestamp:
             # Check if the user has reached otp try limit  
             if  user_max_tries:
                existing_token.otp_try_date = timezone.now() + timezone.timedelta(minutes=30) 
                existing_token.save()
                return Response({'error':'You have exceeded maximum otp requests please try again later'},
                                 status=status.HTTP_429_TOO_MANY_REQUESTS)
             else:
                existing_token.otp = token
                existing_token.max_otp_tries = existing_token.max_otp_tries-1
                existing_token.save()
                resp = convo.send()
                ok =  resp.get('ok',True)
                error = resp.get('error',None)

                if ok:
                    return Response({'message':f'A Verification code has been sent to your phone {str(phone)} via sms'})
                else :
                    return Response({'error':'We are experiencing technical issues and delays at the moment. Please try again later'},
                                 status=status.HTTP_429_TOO_MANY_REQUESTS)
                       
        except OtpSmsToken.DoesNotExist:
            pass

        validate = {'mobile_number':phone ,'otp':token}
        
        #Serialize the data
        serializer = self.get_serializer(data=validate)
        serializer.is_valid(raise_exception=True)

        # Serializer check passed
        # Search if a user has the given mobile number
        try:
            user = User.objects.get(mobile_number=phone)
            if user.mobile_number == phone:
                return Response({'error':f'Account with phone number {phone} already exists'},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        resp = convo.send()
        ok =  resp.get('ok',True)
        error = resp.get('error',None)
       
        if not ok:
            if error != None:
                return Response({'error':f'Country code is not supported. Found error {error}'},
                                status=status.HTTP_400_BAD_REQUEST) 
            return Response({'error':'We are experiencing technical issues and delays at the moment. Please try again later'},
                                 status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        self.perform_create(serializer)  
        return Response({'message':f'A Verification code has been sent to {phone} via sms'},
                         status=status.HTTP_201_CREATED) 
    
class VerifyOTPView(generics.UpdateAPIView):
    serializer_class = OtpSmsTokenSerializer
    model = OtpSmsToken
    permission_classes = (AllowAny,)

    def post(self,request,*args,**kwargs):
        otp = request.data.get('otp', None)
        phone = request.data.get('mobile_number', None)

        if otp == None or phone == None:
            return Response({'error':'Missing Credentials'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item  = OtpSmsToken.objects.get(mobile_number=phone)
            otp = str(otp)
            is_code_valid = check_password(otp,item.otp)
            if not is_code_valid:
                 return Response({'error':'Invalid One Time Password'},status=status.HTTP_400_BAD_REQUEST)
            item.verified = True
            item.save()
            return Response({'message':f'Phone number has been verified successfully!'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f'Found Error {e}')
            return Response({'error':'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)
               
        
    def put(self,request,*args,**kwargs):
        return Response({'error':'Unsupported Request'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def delete(self,request,*args,**kwargs):
        return Response({'error':'Unsupported Request'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def patch(self,request,*args,**kwargs):
        return Response({'error':'Unsupported Request'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@method_decorator(csrf_exempt, name='dispatch')
class KaziUSSDView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = USSDRequestSerializer
    
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        phoneNumber = data.get('phoneNumber',None) 
        text = data.get('text','')
        sessionId = data.get('sessionId',None)
        serviceCode  = data.get('serviceCode',None)
        
        print(f'{phoneNumber} {sessionId} {text} {serviceCode}')

        sender =  self.__class__

        kaziussd = KaziUSSDActions(phoneNumber=phoneNumber,text=text,sender=sender)
        message = kaziussd.switchAction()

        return HttpResponse(message)