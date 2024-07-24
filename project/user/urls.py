from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, Register, Login, LogoutView, Landing, WelcomeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register-api'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', Landing.as_view() , name='landing_page' )
]
