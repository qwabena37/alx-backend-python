
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant, IsMessageSenderOrReadOnly
from .auth import APIKeyAuthentication
from .permissions import IsAuthenticatedCustom 
from .permissions import IsMessageSenderOrReadOnly
from rest_framework import viewsets
from .permissions import IsConversationParticipant, IsMessageSenderOrReadOnly
from .pagination import MessagePagination

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageSenderOrReadOnly]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)
    
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [APIKeyAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageSenderOrReadOnly]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)
    
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    pagination_class = MessagePagination 

    def get_queryset(self):
        conversation_id = (
            self.request.query_params.get("conversation_id")
            or self.request.data.get("conversation_id")
        )
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).order_by("-timestamp") 
    

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
