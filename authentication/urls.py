from django.urls import path
from rest_framework import routers
from .views import (
    RegisterView, VerifyEmail, LoginView, RequestPasswordResetAPIView, PasswordTokenValidatorAPIView, SetNewPasswordAPIView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='registration'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password-email/', RequestPasswordResetAPIView.as_view(), name='reset-password-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenValidatorAPIView.as_view(), name='password-reset'),
    path('password-reset-form', SetNewPasswordAPIView.as_view(), name='password-reset-form'),
]

