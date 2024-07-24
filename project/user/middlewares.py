from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser, User
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = JWTAuthentication()
        try:
            user, validated_token = auth.authenticate(request)
            request.user = user
        except (InvalidToken, TokenError) as e:
            request.user = None

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            try:
                token = AccessToken(access_token)
                user_id = token['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
            except Exception:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
