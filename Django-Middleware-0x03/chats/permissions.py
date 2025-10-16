from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to 
    send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated.
        """
        # Only authenticated users can access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to check if the user is a participant of the conversation
        for PUT, PATCH, or DELETE actions.
        """
        # Check that the user is a participant in the conversation for PUT, PATCH, and DELETE
        if view.action in ['PUT', 'PATCH', 'DELETE']:
            conversation = obj.conversation 
            if request.user not in conversation.participants.all():
                raise PermissionDenied("You are not a participant in this conversation.")
        
        return True
