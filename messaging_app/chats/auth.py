# messaging_app/chats/auth.py

from rest_framework_simplejwt.tokens import RefreshToken

def create_jwt_for_user(user):
    """
    Utility function to create JWT tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
