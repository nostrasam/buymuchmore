from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='user_register'),
    path('login/',CustomUserLoginView.as_view(),name='login'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('user_verify_email/', CustomUserVerificationView.as_view(),name='verify'),
    path('resend-email/',ResendEmailVerificationView.as_view(),name="resend_email"),
    path('password-reset/', PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/<str:uidb64>/<str:token>/',PasswordResetConfirmView.as_view(),name='password_reset'),
    path('logout-single-session/',LogoutSingleSessionView.as_view(),name='logout_single_session'),
    path('logout-all-session/',LogoutAllSessionsView.as_view(),name='logout_all_session')

]