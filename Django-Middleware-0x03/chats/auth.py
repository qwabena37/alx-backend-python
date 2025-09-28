# chats/auth.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class APIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication using X-API-KEY header.
    """
    def authenticate(self, request):
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            return None  # fallback to other authentication methods

        if api_key != "my-secret-key":  # replace with real logic
            raise AuthenticationFailed("Invalid API Key")

        try:
            user = User.objects.get(username="admin")  # assign a user
        except User.DoesNotExist:
            raise AuthenticationFailed("No such user")

        return (user, None)
