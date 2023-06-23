from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    
    def __str__(self) -> str:
        return f'Hi, {self.first_name} {self.last_name} your account is created now!'
    
    def token(self) -> None:
        refresh = RefreshToken.for_user(self)
        return {
            "refresh" : str(refresh),
            "access" : str(refresh.access_token)
        }
        