from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from auth_jwt.serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView

# Create your views here.
class UserRegistrationView(APIView):
    serializer_class = UserRegisterSerializer
    authentication_classes = [JWTAuthentication,]
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                "message" : "Created successfully",
                "user" : serializer.data
            }

            return Response(response, status=status_code)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    authentication_classes = [JWTAuthentication,]
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            email = request.data['username']
            password = request.data['password']
            user = authenticate(username=email, password=password)
            login(request, user)

            response = {
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'user' : user.username
                }

            print(response)

            return Response(response, status=status.HTTP_200_OK)
