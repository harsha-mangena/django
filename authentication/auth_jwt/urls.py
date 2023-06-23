from .views import UserLoginView, UserRegistrationView
from django.urls import path, include

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"), 
    path('login/', UserLoginView.as_view(), name="login"),
]