from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]