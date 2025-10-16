from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager

User = get_user_model()



# Message model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_sent', related_query_name='%(app_label)s_%(class)s_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_messages', related_query_name='%(app_label)s_%(class)s_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)  # Timestamp of the last edit
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')
    parent_message = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    read = models.BooleanField(default=False)
    
    # Use the custom manager
    unread_messages = UnreadMessagesManager()
    
    
    def __str__(self):
        return f'Message from {self.sender.first_name} {self.sender.last_name} to {self.sender.first_name} {self.sender.last_name} at {self.timestamp}'


# Notification model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Notification for {self.user.first_name} {self.user.last_name} about message from {self.user.first_name} {self.user.last_name}' 


# Message history model
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_history', related_query_name='%(app_label)s_%(class)s_history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'History for Message {self.message.id} at {self.timestamp}'       
