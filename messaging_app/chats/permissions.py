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