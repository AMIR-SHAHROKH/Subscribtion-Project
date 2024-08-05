from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, MyTokenObtainPairSerializer
from rest_framework import status
from django.views.generic import DetailView
from user.middlewares import JWTAuthenticationMiddleware 
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

        response = Response({
            'refresh': refresh_token,
            'access': access_token,
            'username': user.username
        }, status=201)
        
        # Set the tokens in cookies
        response.set_cookie('access_token', access_token, httponly=True)
        response.set_cookie('refresh_token', refresh_token, httponly=True)
        
        return response

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        response = Response({
            'refresh': refresh_token,
            'access': access_token,
            'username': user.username
        }, status=200)
        
        # Set the tokens in cookies
        response.set_cookie('access_token', access_token, httponly=True)
        response.set_cookie('refresh_token', refresh_token, httponly=True)
        
        return response

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            
            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Register(TemplateView):
    template_name = 'user/register.html'

class WelcomeView(TemplateView):
    template_name = 'user/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context

class Login(TemplateView):
    template_name = 'user/login.html'
class Landing(TemplateView):
    template_name = 'user/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context['username'] = user.username
            context['is_active_subscription'] = user.is_active_subscription

            if user.is_active_subscription:
                context['progress_percentage'] = (user.days_passed / user.total_days) * 100 if user.total_days > 0 else 0
                context['days_passed'] = user.days_passed
                context['days_left'] = user.days_left
                context['total_days'] = user.total_days
            else:
                context['progress_percentage'] = 0
                context['days_passed'] = 0
                context['days_left'] = 0
                context['total_days'] = 0
        else:
            context['username'] = None
            context['progress_percentage'] = 0
            context['days_passed'] = 0
            context['days_left'] = 0
            context['total_days'] = 0

        return context

