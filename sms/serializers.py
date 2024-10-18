from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import OtpSmsToken

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