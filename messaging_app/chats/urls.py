"""Imports for chats/urls.py"""
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import ConversationViewSet, MessageViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# Router setup
router = routers.DefaultRouter()

# Main router for conversations
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
conversations_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r"messages", MessageViewSet, basename="conversation-messages")





urlpatterns = [
    path('', include(router.urls)),
    path("", include(conversations_router.urls)),
    
    # Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]