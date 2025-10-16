from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django_filters import rest_framework as filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .permissions import IsOwner
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination
from .filters import MessageFilter

User = get_user_model()

# Filter class for filtering Conversations
class ConversationFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Conversation
        fields = ['created_after', 'created_before']

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ConversationFilter
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Create a conversation and add participants
        conversation = serializer.save()
        participants = self.request.data.get("participants", [])
        for user_id in participants:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Filter class for filtering Messages
class MessageFilter(filters.FilterSet):
    sent_after = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sent_after', 'sent_before']

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    
    def get_queryset(self):
        """
        Return messages that belong only to the logged-in user's conversations.
        This filters messages based on the conversation the user is a participant of.
        """
        conversation_id = self.kwargs.get('conversation_id')

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation does not exist."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if the user is a participant of the conversation
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Return messages related to the conversation the user is a part of
        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        """
        Ensure the user is a participant of the conversation before creating a message.
        """
        conversation_id = self.kwargs.get('conversation_id')

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation does not exist."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Ensure the user is a participant of the conversation
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Save the message with the user and conversation information
        serializer.save(user=self.request.user, conversation=conversation)

    def perform_update(self, serializer):
        """
        Override update to ensure the user is a participant of the conversation
        before allowing the message update.
        """
        conversation_id = self.kwargs.get('conversation_id')

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation does not exist."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Ensure the user is a participant of the conversation
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Save the updated message
        serializer.save()

    def perform_destroy(self, instance):
        """
        Override destroy to ensure the user is a participant of the conversation
        before allowing the message deletion.
        """
        conversation_id = self.kwargs.get('conversation_id')

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation does not exist."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Ensure the user is a participant of the conversation
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Proceed with deleting the message
        instance.delete()