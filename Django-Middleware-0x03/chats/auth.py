# messaging_app/chats/auth.py

from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

def create_jwt_for_user(user):
    """
    Utility function to create JWT tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    
    # Use the settings for token expiration times
    refresh.set_exp(lifetime=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
    refresh.access_token.set_exp(lifetime=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
