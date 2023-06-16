import base64
from datetime import datetime

# import pyotp
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken

# from account.tasks import send_email

from .models import OtpVerify, User
from rest_framework.validators import UniqueValidator


class generateKey:
    @staticmethod
    def returnValue(userObj):
        return str(timezone.now())+ str(datetime.date(datetime.now())) + str(userObj.id)


class UserListCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, required = True, write_only = True)
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone',
            'email',
            'password',
            
        ]
        read_only_field = ['id']
        extra_kwargs = {
            'phone':{'required': True},
        }
        
        def validate(self,attrs):
            email = attrs.get('email',None)
            request = self.context.get('request')
            if request.method == "POST":
                if User.objects.filter(email__iexact=email()):
                    return serializers.ValidationError('Email already exist! Please, try another email')
            
            return attrs
        
        def create(self,validated_data):
            
            newuser = User.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                full_name=str(validated_data['first_name']) +
                ' '+str(validated_data['last_name']),
                phone=validated_data['phone'],
                email=validated_data['email'],
                # user_role=validated_data['user_role'],
                is_verified=True,
                is_active=True,
                is_approved=True,
            )
            newuser.set_password(validated_data['password'])
            newuser.save()
            return newuser


class UserDetailViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email","phone"]

        read_only_field = ['id', 'email']        



class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=120, required=True, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=5, write_only=True)
    access_token = serializers.CharField(
        max_length=200, min_length=5, read_only=True)
    refresh_token = serializers.CharField(
        max_length=200, min_length=5, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'access_token',
                  'refresh_token']
        read_only_fields = ['access_token', 'refresh_token', ]

  
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "provided credentials are not valid/email"}, code=status.HTTP_401_UNAUTHORIZED)

        if user:
            if not user.check_password(password):
                raise serializers.ValidationError(
                    {"password": "provided credentials are not valid/password"}, code=status.HTTP_401_UNAUTHORIZED)
        if not user:
            raise serializers.ValidationError(
                {"email": "User not found"}, code=status.HTTP_401_UNAUTHORIZED)

        token = RefreshToken.for_user(user)
        attrs['id'] = int(user.id)
        attrs['first_name'] = str(user.first_name)
        attrs['last_name'] = str(user.last_name)
        attrs['username'] = str(user.full_name)
        attrs['phone'] = str(user.phone)
        attrs['email'] = str(user.email)
        attrs['is_owner'] = str(user.is_owner)
        attrs['access_token'] = str(token.access_token)
        attrs['refresh_token'] = str(token)
        return attrs
        