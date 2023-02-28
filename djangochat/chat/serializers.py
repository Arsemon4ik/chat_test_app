from .models import User, Message, Thread
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'


class ThreadListSerializer(serializers.ModelSerializer):
    # initiator = UserSerializer()
    # receiver = UserSerializer()
    # participants = serializers.StringRelatedField(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['participants', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        print(message)
        if message:
            return MessageSerializer(instance=message).data
        else:
            return "No messages yet"