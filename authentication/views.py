from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView 
from rest_framework import status, views
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer)
from django.utils.http import (
    urlsafe_base64_decode, urlsafe_base64_encode)
from django.utils.encoding import (
    smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError)
from rest_framework.reverse import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User
from .utils import Util
from .renderers import UserRenderer
import jwt

# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    #The first thing we built.
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('authentication:verify-email')
        absurl = 'http://'+current_site+'/'+relative_link+'/?token='+str(token)
        email_body = 'Hi '+user.username+' please use the link below to verify your email! \n'+absurl
        data = {
            'email_body': email_body, 
            'to_mail': user.email, 
            'email_subject': 'Email Verification'
            }
        
        Util.send_email(data)
        return Response(user_data, status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    #Here we are going to define our swager parameter.
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully Activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetAPIView(GenericAPIView):

    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relative_link = reverse(
                'authentication:password-reset', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relative_link
            email_body = 'Hello, use this link to reset your password ' + absurl
            data = {
                'email_body': email_body,
                'to_mail': user.email,
                'email_subject': 'Restore your password!'
            }
            Util.send_email(data)
            return Response({'Sucess': 'We alredy sent you a mail which will allow you to restore your password!'}, status=status.HTTP_200_OK)
        else:
            return Response({'Error':'An invalid email was provided.'})
    

#This endpoint allows us to verify the provided mail credentials.
class PasswordTokenValidatorAPIView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'Error': 'An invalid token was provided. Please, request a new one!'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'Success': True, 'Message': 'Valid credentials', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'Error': 'An invalid token was provided. Please, request a new one!'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'Success':'You password, was updated!'}, status=status.HTTP_200_OK)
