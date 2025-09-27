# chats/permissions.py
from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission: only allow participants of a conversation to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        # obj here will be a Conversation instance
        return request.user in obj.participants.all()

from rest_framework import permissions

class IsMessageSenderOrReadOnly(permissions.BasePermission):
    """
    Only the sender can edit/delete their message.
    Other participants can read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.conversation.participants.all()
        return obj.sender == request.user

from rest_framework import permissions

class IsAuthenticatedCustom(permissions.BasePermission):
    """
    Custom permission: only allow access to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    # chats/permissions.py
from rest_framework import permissions

class IsMessageSenderOrReadOnly(permissions.BasePermission):
    """
    Only the sender can edit/delete their message.
    Other participants can read.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]
        if request.method in permissions.SAFE_METHODS:
            # allow read-only access if user is in the conversation
            return request.user in obj.conversation.participants.all()
        

        # restrict PUT, PATCH, DELETE to sender only
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.sender == request.user

        return False

# chats/permissions.py
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from .models import Message, Conversation

class IsConversationParticipant(permissions.BasePermission):
    """
    Allow access only if user is authenticated and belongs to the conversation.
    """

    def has_permission(self, request, view):
        # Must be logged in
        if not request.user or not request.user.is_authenticated:
            return False

        # conversation_id must be present in request data or query params
        conversation_id = (
            request.data.get("conversation_id")
            or request.query_params.get("conversation_id")
        )
        if not conversation_id:
            raise PermissionDenied(
                detail="conversation_id is required",
                code=status.HTTP_403_FORBIDDEN,
            )

        # Verify the user is a participant of the conversation
        if not Message.objects.filter(
            id=conversation_id, participants=request.user
        ).exists():
            raise PermissionDenied(
                detail="You are not part of this conversation",
                code=status.HTTP_403_FORBIDDEN,
            )

        return True
