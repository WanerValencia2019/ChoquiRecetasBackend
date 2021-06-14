from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
#from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView,UpdateAPIView
#from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
#from django.contrib.auth import login
from .models import CustomModelUser, CodeVerification
from threading import Thread

from .mail import Mail

User = CustomModelUser
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import SessionAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

#REGISTER
class CreateUserVIEW(GenericAPIView):
    serializer_class=CreateUserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    
    def post(self,request):
        #print(request)
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        print(user.email)

        codeVerification = CodeVerification.objects.create_code_verification(User, user.email)

        thread = Thread(target=Mail.send_code_verification, args=(
            user, codeVerification
            ))
        thread.start()
        return Response({"message":"A verification code has been sent to your email"},status.HTTP_200_OK)

# CODE VERIFICATION
class CodeVerificationView(GenericAPIView):
    serializer_class = CodeVerificationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    
    def post(self,request):
        #print(request)
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data=serializer.data
        print(data)
        return Response({"message":"Cuenta verificada con éxito"},status.HTTP_200_OK)

#LOGIN
class LoginView(GenericAPIView):
    serializer_class=LoginSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        self.headers.setdefault("X-CSRFToken",get_token(request))
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data
        token=Token.objects.get_or_create(user=user)
        key=token[0].key
        login(self.request,user)
        print(self.headers)
        userSerialized = UserSerializer(user,context=self.get_serializer_context()).data
        return Response({"user":userSerialized,"token":key},status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def post(self,request):
        self.headers.setdefault("X-CSRFToken",get_token(request))
        user=request.user
        logout(request)
        user.auth_token.delete()
        return Response({"User":"Sesión terminada"},status.HTTP_200_OK)

class SendCodeVerification(GenericAPIView):
    serializer_class = SendCodeVerificationSerializer
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
    serializer_class = SendCodeVerificationSerializer
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


class ResetPasswordVerifyCodeView(GenericAPIView):
    serializer_class = ResetPasswordVerifyCodeSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("DATA")
        return Response({"message":"We have sent an email with your new password"},status.HTTP_200_OK)


#CAMBIANDO LA CONTRASEÑA DEL USUARIO
class ChangePasswordView(UpdateAPIView):
    serializer_class=ChangePasswordSerializer
    #model=User
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get_object(self,queryset=None):
        user=self.request.user
        return user
#CAMBIANDO EL NOMBRE DEL USUARIO


class ChangeNamesView(UpdateAPIView):
    serializer_class=ChangeNamesSerializer
    model=User
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get_object(self,queryset=None):
        user=self.request.user
        return user

class ChangeUsernameView(UpdateAPIView):
    serializer_class=ChangeUsernameSerializer
    model=User
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get_object(self,queryset=None):
        user=self.request.user
        return user

class ChangeEmailView(UpdateAPIView):
    serializer_class=ChangeEmailSerializer
    model=User
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)
    def get_object(self,queryset=None):
        user=self.request.user
        return user

class UserInfo(APIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes=(TokenAuthentication,)

    def get(self,request):
        serializer=UserSerializer(request.user)
        token=Token.objects.get(user=request.user)
        print(token)
        user=serializer.data
        print(serializer.data)
        return  Response({"User":user,"Token":token.key},status.HTTP_200_OK)