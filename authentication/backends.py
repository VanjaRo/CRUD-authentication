import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.fields import NOT_READ_ONLY_REQUIRED


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_data = authentication.get_authorization_header(request)
        auth_header = auth_data.split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        if not auth_data:
            return None

        if len(auth_header) == 1 or len(auth_header) > 2:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
        except Exception:
            msg = 'Authentication Error: could not decode your token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'Authentication Error: could not find any user with this token.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'Authentication Error: user with this token is deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
