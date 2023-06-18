from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True, null=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self) -> str:
        return "Hi, {} {} your account is created".format(self.first_name, self.last_name)

    def token(self) -> None:
        refresh = RefreshToken.for_user(self)
        return {
            "refresh" : str(refresh),
            "access" : str(refresh.access_token)
        }