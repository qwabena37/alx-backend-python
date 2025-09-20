from rest_framework import viewsets, status, filters
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing conversations and creating new ones
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages and sending messages to existing conversations
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer