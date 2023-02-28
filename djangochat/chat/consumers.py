import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.core.files.base import ContentFile

from django.contrib.auth.models import User
from .models import Message, Thread
from .serializers import MessageSerializer


# class ChatConsumer(AsyncWebsocketConsumer):
#     print("CONNECTED")
#     pass
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("here")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        thread = Thread.objects.get(id=int(self.room_name))
        participants_of_thread = thread.participants.all()

        current_user = self.scope['user']
        if current_user.is_authenticated and current_user in participants_of_thread:
            # Join room group if user in participants
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()
        else:
            # close connection to the other users
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)

        # Send message to room group
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    # Receive message from room group
    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        # message = text_data_json['message']
        message = text_data_json.get("message", None)

        if message is None:
            self.send(
                text_data=json.dumps({"Warning": "To send message - use 'message' in the body!"})
            )

        thread = Thread.objects.get(id=int(self.room_name))
        sender = self.scope['user']

        _message = Message.objects.create(
            sender=sender,
            text=message,
            thread=thread,
        )
        serializer = MessageSerializer(instance=_message)
        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                serializer.data
            )
        )
