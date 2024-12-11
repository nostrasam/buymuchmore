from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


class UserRegisterSerializer(serializers.ModelSerializer):
    username=None
    password = serializers.CharField(write_only=True, validators=[validate_password],required=True)
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = CustomUser
        fields = ('email','password','password2','first_name','last_name','phone_number',)

    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is Already In Use')
        return value
    
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"passwords: Passwords do not match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number']
        )
        user.is_active=False
        user.set_password(validated_data['password'])
        user.save()
        return user



class CustomUserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add custom claims
        token['email'] = user.email
        return token
    
    def validate(self, data):
        email = data.get('email',None)
        password = data.get('password',None)

        if not email:
            raise AuthenticationFailed({'email':'An email address is Required'})
        
        if not password:
            raise AuthenticationFailed({'password':'A Password is Required'})
        
        try:
             user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
           raise serializers.ValidationError({'email':'This email is not registered, Please Sign Up'})
        
        if not user.check_password(password):
             raise serializers.ValidationError('Password incorrect')
        
        if not user.is_active:
            raise serializers.ValidationError({'verification':'User has registered, Please conclude the email verification'})
        
        data = super().validate(data)
        return data
 
    

class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email']

    def validate_email(self, value):
        email = value.lower()  # Normalize email
        try:
            self.user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('No user found with this email address.')
        return email



class PasswordConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(write_only=True, required=True)


    def validate(self,data):
        uidb64 = data['uidb64']
        token = data['token']
        new_password = data['new_password']

        # decode the user from UID
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except(TypeError,ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError({'token':'Invalid UID'})
        

        # validate the token
        if not default_token_generator.check_token(user,token):
            raise serializers.ValidationError({'token':'Invalid or expired token'})
        
        # validate the new password
        try:
            validate_password(new_password, user=user)
        except serializers.ValidationError as error:
            raise serializers.ValidationError({'new_password':error.messages})
        

    def save(self):
        # save the new password for the user
        user = self.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        
    