from django.shortcuts import render
from .models import CustomUser,CustomUserVerification
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework import status
from django.urls import reverse
from .tasks import *
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .tasks import user_reset_password_send_email_task
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken,BlacklistedToken


# Create your views here.


class UserRegistrationView(APIView):
    serializer_class = UserRegisterSerializer
    queryset = CustomUser.objects.all()
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'user':serializer.data, 'message': 'User Created Successfully'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class CustomUserLoginView(TokenObtainPairView):
    serializer_class = CustomUserLoginSerializer



class CustomUserVerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return Response({'message': 'Token is required'}, status=400)
        
        if CustomUser.objects.filter(email=self.request.user.email, is_active=True).exists():
             return Response({'message': 'User has already been verified'}, status=400)

        try:
            verification = CustomUserVerification.objects.get(verification_token=token)
        except CustomUserVerification.DoesNotExist:
            return Response({'message': 'Invalid or expired token'}, status=400)

        # Mark as verified and update the vendor profile
        verification.is_verified = True
        verification.verification_token = None
        verification.save()

        user_profile = CustomUserVerification.objects.get(user=verification.user)
        user_profile.is_active = True
        user_profile.save()

        return Response({'message': 'Email verified successfully'}, status=200)


class ResendEmailVerificationView(APIView):
    def post(self, request,*args,**kwargs):
        user = self.request.user
        try:
            customuser = CustomUser.objects.filter(email=user.email)
            if customuser.is_active:
                return Response({'message':'User has already verified this account successfully'})
        except CustomUser.DoesNotExist:
            return Response({'message':'Email not found, Please register firstv'})
        
        token = CustomUserVerification.objects.get(user=user).verification_token

        verification_url = f"https://buymuchmore.com/mainauth/{reverse('verify', args=[token])}"
        user_register_send_email_task.delay(user.email,verification_url)
        return Response({'message':'Verification email has been resent'})


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.user  # Retrieve the validated user
            self.send_reset_mail(user)  # Pass the user to the method
            return Response({'message': 'Password Reset email sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_reset_mail(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"https://buyuchmore.com/reset_password/{uid}/{token}"

        # Asynchronously send the email using Celery
        user_reset_password_send_email_task.delay(user.email, reset_url)



class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordConfirmSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LogoutSingleSessionView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message':'User has been logged out'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'message':'An error occured'},status=status.HTTP_400_BAD_REQUEST)
        


class LogoutAllSessionsView(APIView):
    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response({'message':'User has been logged out from all devices'},status=status.HTTP_205_RESET_CONTENT)
