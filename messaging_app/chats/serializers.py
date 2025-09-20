from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'first_name',
            'last_name', 'phone_number', 'role', 'created_at', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'user_id': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
        """
        Create user with encrypted password
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model with sender details
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation',
            'message_body', 'sent_at'
        ]
        extra_kwargs = {
            'message_id': {'read_only': True},
            'sent_at': {'read_only': True},
        }

    def create(self, validated_data):
        """
        Create message with sender from request context
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['sender'] = request.user
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested relationships
    """
    participants = UserSerializer(many=True, read_only=True)
    participants_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participants_ids',
            'messages', 'last_message', 'created_at'
        ]
        extra_kwargs = {
            'conversation_id': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def get_last_message(self, obj):
        """
        Get the most recent message in the conversation
        """
        last_message = obj.messages.first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def create(self, validated_data):
        """
        Create conversation and add participants
        """
        participants_ids = validated_data.pop('participants_ids', [])
        conversation = Conversation.objects.create()

        # Add current user as participant
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            conversation.participants.add(request.user)

        # Add other participants
        if participants_ids:
            users = User.objects.filter(user_id__in=participants_ids)
            conversation.participants.add(*users)

        return conversation


# Simplified serializer for list views
class ConversationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for conversation lists
    """
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'last_message',
            'message_count', 'created_at'
        ]

    def get_last_message(self, obj):
        last_message = obj.messages.first()
        if last_message:
            return {
                'message_body': last_message.message_body,
                'sent_at': last_message.sent_at,
                'sender': last_message.sender.email
            }
        return None

    def get_message_count(self, obj):
        return obj.messages.count()