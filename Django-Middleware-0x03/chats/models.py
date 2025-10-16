from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
import uuid

# User model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, db_index=True)
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=128, null=False, blank=False) # This field is not usually hardcoded in django
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=False, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    # Use email instead of username for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        """Class for defining user table constraints and indexes"""
        db_table = 'user'
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_user_email')
        ]
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_id'])
        ]
    
    def __str__(self):
        return f'Name: {self.first_name} {self.last_name} ({self.email})'
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

# Conversation model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Class for defining conversation table indexes"""
        db_table = 'conversation'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['conversation_id'])
        ]
    
    def __str__(self):
        return f"Conversation {self.conversation_id} with {', '.join([str(user) for user in self.participants.all()])}"

# Message model
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', null=False, db_index=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=False, db_index=True)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Class for defining message table indexes"""
        db_table = 'message'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=["sender", "sent_at"]),
            models.Index(fields=["conversation", "sent_at"]),
            models.Index(fields=["sent_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(message_body__isnull=False) & ~models.Q(message_body=''),
                name="message_body_not_empty"
            )
        ]
    
    def __str__(self):
        return f"Message {self.message_id} from {self.sender} in conversation {self.conversation_id}"    
