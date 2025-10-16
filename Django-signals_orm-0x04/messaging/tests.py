# messaging/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessageNotificationTest(TestCase):

    def setUp(self):
        # Create users for testing
        self.sender = User.objects.create_user(full_name='sender', password='password123')
        self.receiver = User.objects.create_user(full_name='receiver', password='password123')

    def test_notification_creation_on_message_send(self):
        # Send a message from sender to receiver
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello, World!")

        # Check if a notification is created for the receiver
        notification = Notification.objects.get(user=self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.seen) 

class UserDeletionTest(TestCase):

    def setUp(self):
        # Create users for testing
        self.user = User.objects.create_user(full_name='testuser', password='password123')
        self.receiver = User.objects.create_user(full_name='receiver', password='password123')

        # Create related data
        self.message = Message.objects.create(sender=self.user, receiver=self.receiver, content="Hello!")
        self.notification = Notification.objects.create(user=self.receiver, message=self.message)
        self.history = MessageHistory.objects.create(message=self.message, old_content="Hello!")

    def test_user_deletion_clears_related_data(self):
        # Ensure data exists before deletion
        self.assertTrue(Message.objects.exists())
        self.assertTrue(Notification.objects.exists())
        self.assertTrue(MessageHistory.objects.exists())

        # Delete the user
        self.user.delete()

        # Check that related data is deleted
        self.assertFalse(Message.objects.exists())
        self.assertFalse(Notification.objects.exists())
        self.assertFalse(MessageHistory.objects.exists())