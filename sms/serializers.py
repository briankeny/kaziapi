from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import OtpSmsToken
from phonenumber_field.serializerfields import PhoneNumberField

class OtpSmsTokenSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True)  
    
    # Exclude otp from serialization
    def create(self, validated_data):

        # Remove otp from validated data
        tkn = validated_data.pop('otp')
        # Hash the token
        hashed_otp = make_password(tkn)  
        validated_data['otp'] = hashed_otp
        return super().create(validated_data)    

    class Meta:
        model = OtpSmsToken
        fields = '__all__'

class USSDRequestSerializer(serializers.Serializer):
    phoneNumber =  PhoneNumberField(required=True, max_length=15)
    text = serializers.CharField(required=False, allow_blank=True)
    sessionId = serializers.CharField(required=False, allow_blank=True)
    serviceCode = serializers.CharField(required=False, allow_blank=True)

    