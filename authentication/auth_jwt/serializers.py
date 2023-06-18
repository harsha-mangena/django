from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']

class UserRegisterSerializer(serializers.ModelSerializer):
    PASSWORD_HELP_TEXT = "Please include the numbers and symbols for the strong password."
    
    password = serializers.CharField(required=True, write_only=True, min_length=8, max_length=60, help_text=PASSWORD_HELP_TEXT)
    retyped_password = serializers.CharField(required=True,write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'retyped_password']
    
    def validate(self, validated_data):
        if validated_data['password'] != validated_data['retyped_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return validated_data

    def create(self, validated_data, username = None):
        validated_data.pop('retyped_password', None)
        username = validated_data['email']
        validated_data['username'] = username
        
        validated_data.pop('email')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        
        user.set_password(password)
        
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'access', 'refresh']
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        
        try:
            login(user)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username
            }

            return validation

        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

        
