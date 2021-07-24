from threading import Thread

from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
#from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView,UpdateAPIView
from rest_framework.authentication import SessionAuthentication 
#from django.contrib.auth.models import User
#from django.views.decorators.csrf import csrf_protect
#from django.contrib.auth import login
from .models import CustomModelUser, CodeVerification, Follower
from .mail import Mail
from . import serializers
User = CustomModelUser

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

#REGISTER
class CreateUserVIEW(GenericAPIView):
    serializer_class= serializers.CreateUserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        #print(request)
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()    
        #print(user.email)
        codeVerification = CodeVerification.objects.create_code_verification(User, user.email)
        thread = Thread(target=Mail.send_code_verification, args=(
            user, codeVerification
            ))
        thread.start()
        return Response({"message":"A verification code has been sent to your email"}, status.HTTP_201_CREATED)

class ChangeImageProfileView(GenericAPIView):
    serializer_class= serializers.ChangeImageProfileSerializer
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_serialized = serializers.UserSerializer(user,context={"request":self.request})
        data=user_serialized.data    
        return Response({"image_url":data.get('image_profile')}, status.HTTP_200_OK)

# CODE VERIFICATION
class CodeVerificationView(GenericAPIView):
    serializer_class = serializers.CodeVerificationSerializer
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication,)
    
    def post(self,request):
        #print(request)
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message":"Cuenta verificada con éxito"},status.HTTP_200_OK)

#LOGIN
class LoginView(GenericAPIView):
    serializer_class=serializers.LoginSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        self.headers.setdefault("X-CSRFToken",get_token(request))
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data
        token=Token.objects.get_or_create(user=user)
        key=token[0].key
        login(self.request, user)
        print(self.headers)
        userSerialized = serializers.UserSerializer(user,context=self.get_serializer_context()).data
        return Response({"user":userSerialized,"token":key},status.HTTP_200_OK)

class ProfileView(GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication, CsrfExemptSessionAuthentication)

    def get(self, request, format=None):
        user = self.get_serializer(instance=self.request.user)
        user.is_valid(raise_exception=True)
        data = user.data
        return Response(data,status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication, CsrfExemptSessionAuthentication)
    def post(self,request):
        self.headers.setdefault("X-CSRFToken",get_token(request))
        user = request.user
        logout(request)
        user.auth_token.delete()
        return Response({"User":"Sesión terminada"},status.HTTP_200_OK)

class SendCodeVerification(GenericAPIView):
    serializer_class = serializers.SendCodeVerificationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)    

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data=serializer.data
        user = User.objects.filter(email=data['email']).first()
        codeVerification = CodeVerification.objects.filter(user=user).first()
        
        thread = Thread(target=Mail.send_code_verification, args=(
            user,codeVerification
            ))
        thread.start()
        return Response({"message":"A verification code has been sent to your email"},status.HTTP_200_OK)

class ResetPasswordSendCodeView(GenericAPIView):
    serializer_class = serializers.SendCodeVerificationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data=serializer.data
        user = User.objects.filter(email=data['email']).first()
        code_verification = CodeVerification.objects.filter(user=user).first()
        thread = Thread(target=Mail.send_code_verification, args=(
            user, code_verification
            ))
        thread.start()
        return Response({"message":"A verification code has been sent to your email"},status.HTTP_200_OK)


class ResetPasswordVerifyCodeView(GenericAPIView):
    serializer_class = serializers.ResetPasswordVerifyCodeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("DATA")
        return Response({"message":"We have sent an email with your new password"},status.HTTP_200_OK)


#CAMBIANDO LA CONTRASEÑA DEL USUARIO
class ChangePasswordView(UpdateAPIView):
    serializer_class=serializers.ChangePasswordSerializer
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    
    def get_object(self,queryset=None):
        user=self.request.user
        return user

#CAMBIANDO EL NOMBRE DEL USUARIO
class ChangeNamesView(UpdateAPIView):
    serializer_class=serializers.ChangeNamesSerializer
    model=User
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get_object(self,queryset=None):
        user=self.request.user
        return user

class ChangeUsernameView(UpdateAPIView):
    serializer_class=serializers.ChangeUsernameSerializer
    model=User
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get_object(self,queryset=None):
        user=self.request.user
        return user

class ChangeEmailView(UpdateAPIView):
    serializer_class=serializers.ChangeEmailSerializer
    model=User
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get_object(self,queryset=None):
        user=self.request.user
        return user

class UserProfileView(APIView):
    serializer_class = serializers.UserSerializer
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication, CsrfExemptSessionAuthentication)

    def get(self,request):
        serializer=serializers.UserSerializer(request.user, context={"request":request})
        token=Token.objects.filter(user=request.user).first()
        user=serializer.data
        return  Response({"user":user,"token":token.key if token is not None else None},status.HTTP_200_OK)