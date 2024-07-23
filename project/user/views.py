from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, MyTokenObtainPairSerializer
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView

CustomUser = get_user_model()

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return response with tokens
        return Response({
            'refresh': refresh_token,
            'access': access_token,
            'username': user.username
        }, status=201)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class Register(TemplateView):
    template_name = 'user/register.html'

class WelecomeView(LoginRequiredMixin, TemplateView):
    template_name = 'user/welcome.html'

class Login(TemplateView):
    template_name = 'user/login.html'