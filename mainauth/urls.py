from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='user_register'),
    path('login/',CustomUserLoginView.as_view(),name='login'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('user_verify_email/', CustomUserVerifyEmailView.as_view(),name='verify')

]