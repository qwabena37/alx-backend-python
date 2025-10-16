from datetime import timezone
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created: # Only trigger when a new message is created
        Notification.objects.create(
            user = instance.receiver,
            message = instance
        )
        
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Check if the message content is being edited (not the first creation)
    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk) # Original content
            
            if original.content != instance.content:  # Check if content is different
                # Create a new history record for the edited message
                MessageHistory.objects.create(
                    message = original,
                    old_content=original.content,
                    edited_by=instance.edited_by,
                )   
                instance.edited = True # Mark the message as edited
                instance.edited_at = timezone.now()
        except Message.DoesNotExist:
            pass      # If the message does not exist, do nothing    


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete all messages where the user is the sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications related to the user
    Notification.objects.filter(user=instance).delete()

    # Delete all message histories related to the user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()         