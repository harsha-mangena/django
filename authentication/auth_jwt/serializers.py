from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8, max_length=30)
    retype_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User 
        fields = ['id', 'username' ,'email', 'first_name', 'last_name', 'password', 'retype_password']
    
    def validated(self, *attrs):
        if attrs.get('password') != attrs.get('retype_password'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('retype_password')
        
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
           
        user.set_password(password)
        
        return user
        
        
class UserLoginSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True,write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'access_token', 'refresh_token']
        
    def validate(self, attrs):
        import pdb; pdb.set_trace();
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
    