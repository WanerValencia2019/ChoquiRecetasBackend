from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Q
from threading import Thread

from .models import CustomModelUser, CodeVerification, Follower
from .utils import get_random_string

from .mail import Mail
from apps.utils import get_binary_content
from apps.recipes.serializers import RecipeSerializer
User = CustomModelUser



class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("uuid","username","first_name","last_name",'image_profile')

class FollowerSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    class Meta:
        model=Follower
        exclude = ('follower','id')

class FollowingSerializer(serializers.ModelSerializer):
    follower = UserShortSerializer(read_only=True)
    class Meta:
        model=Follower
        exclude = ('user','id')


class UserSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True,source="recipe_set")
    followers = FollowerSerializer(many=True, read_only=True,source="user_followed")
    followings = FollowingSerializer(many=True, read_only=True,source="user_follower")
    class Meta:
        model=User
        fields=("id","uuid","username","email","first_name","last_name","followers","followings",'recipes','image_profile')



class CreateUserSerializer(serializers.Serializer):
    id=serializers.ReadOnlyField()
    username=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    first_name=serializers.CharField(required=True)
    email=serializers.EmailField()
    password=serializers.CharField(required=True)
    password_confirm=serializers.CharField(required=True)
    def create(self,validated_data):
        user=User()
        user.username=validated_data.get('username')
        user.first_name=validated_data.get('first_name')
        user.last_name=validated_data.get('last_name')
        user.email=validated_data.get('email')
        user.is_active=False
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def validate(self,validated_data):
        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError({"message":"Las contrase??as no coinciden"})

        users=User.objects.filter(Q(username=validated_data.get('username')) | Q(email=validated_data.get('email')))

        if len(users) != 0:
            raise serializers.ValidationError({"message":"El nombre de usuario Y/O email ya se encuentra registrado"})

        return validated_data

class ChangeImageProfileSerializer(serializers.Serializer):
    image_profile=serializers.CharField(required = True)

    def create(self, validated_data):
        image = get_binary_content(validated_data.get('image_profile'))
        user = self.context['request'].user
        user.image_profile.save("default.jpeg",image, save=False)
        user.save()

        return user

    def validate(self, data):
        image = data.get('image_profile')
        if len(image)%4 != 0:
            raise serializers.ValidationError({"message":"Esta imag??n no es v??lida"}) 
        return data


# CODE VERIFICATION
class CodeVerificationSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    code=serializers.CharField(required=True, max_length=4)

    def validate(self, validated_data):
        code = CodeVerification.objects.verify_code(validated_data['email'],validated_data['code'])

        if code is None:
            raise serializers.ValidationError({"message":"El c??digo verificaci??n es inv??lido"})
        
        code.used = True
        code.save()

        user = User.objects.get(email = validated_data['email'])
        user.is_active = True
        user.save()

        return validated_data

#LOGIN
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

    def validate(self,data):
        user=authenticate(username=data.get('username'),password=data.get('password'))
        if user and user.is_active:
            return user
        elif user and not user.is_active:
            raise serializers.ValidationError({"message":"Esta cuenta est?? inactiva, activa tu cuenta"})
        else:
            raise serializers.ValidationError({"message":"Credenciales incorrectos"})

        return user



#RESET PASSWORD OR ACTIVATE ACCOUNT
class SendCodeVerificationSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)

    def validate(self, validated_data):
        code = CodeVerification.objects.create_code_verification(User, validated_data['email'])

        if code is None:
            raise serializers.ValidationError({"message":"Este correo electr??nico es inv??lido"})
        

        return validated_data  


class ResetPasswordVerifyCodeSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    code=serializers.CharField(required=True, max_length=4)

    def validate(self, validated_data):
        code = CodeVerification.objects.verify_code(validated_data['email'],validated_data['code'])

        if code is None:
            raise serializers.ValidationError({"message":"El c??digo verificaci??n es inv??lido"})
        
        code.used = True
        code.save()
        new_password = get_random_string(12)

        user = User.objects.get(email = validated_data['email'])
        user.set_password(new_password)
        user.save()

        thread = Thread(target=Mail.send_reseted_password, args=(
            user, new_password
            ))
        thread.start()
        
        return validated_data






#cambiando la contrase??a del usuario, CHANGE PASSWORD
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self,validated_data):
        #print(validated_data)
        user=self.context['request'].user
        #print(dir(user))
        old_password=validated_data.get('old_password')
        print(user.check_password(old_password))
        #print(f"{old_password} {user.password}")
        if not(user.check_password(old_password)):
            raise serializers.ValidationError({"message":"La contrase??a actual no es correcta"})

        elif not(validated_data.get('new_password')== validated_data.get('password_confirm')):
            raise serializers.ValidationError({"message":"Las contrase??as no coinciden"})

        elif not (len(validated_data.get('new_password'))>8):
            raise serializers.ValidationError({"message":"La contrase??a debe contener mas caracteres"})
        return validated_data

    def update(self,user,validated_data):
        user.set_password(validated_data.get('new_password'))
        user.save()
        return user

#cambiando el first_name y el last_name
class ChangeNamesSerializer(serializers.Serializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)

    def update(self,user,validated_data):
        user.first_name=validated_data.get('first_name')
        user.last_name=validated_data.get('last_name')
        user.save()
        return user

class ChangeUsernameSerializer(serializers.Serializer):
    username=serializers.CharField(required=True,max_length=15)

    def validate(self,validated_data):
        username=validated_data.get('username')
        exists=User.objects.filter(username=username)

        if len(exists)!=0:
            raise serializers.ValidationError({"message":"El nombre de usuario ya se encuentra en uso"})
        if not(len(username)>=6):
            raise serializers.ValidationError({"message":"El nombre de usuario es muy corto"})
        return validated_data

    def update(self,user,validated_data):
        user.username=validated_data.get('username')
        user.save()
        return user

class ChangeEmailSerializer(serializers.Serializer):
        email=serializers.EmailField(required=True)

        def update(self,user,validated_data):
            user.email=validated_data.get('email')
            user.save()
            return user