import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.renderers import JSONRenderer

from .serialalizers import messageSerializer
from .models import message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    # ---------- commands ----------
    async def new_message(self, data):
        text = data["message"]
        author_name = data["username"]
        message_obj = await self.create_message(author_name, text)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": [message_obj],
            },
        )

    @database_sync_to_async
    def create_message(self, author_name, text):
        user = User.objects.get(username=author_name)
        obj = message.objects.create(author=user, content=text, room_name=self.room_name)
        payload = messageSerializer(obj).data
        return payload

    async def fetch_message(self, data):
        messages = await self.get_last_message(self.room_name)
        await self.send(text_data=json.dumps({"message": messages}))

    @database_sync_to_async
    def get_last_message(self, room_name):
        qs = list(message.last_message(room_name=room_name))
        serialized = messageSerializer(qs, many=True)
        return json.loads(JSONRenderer().render(serialized.data))

    commands = {
        "new_message": new_message,
        "fetch_message": fetch_message,
    }

    # ---------- websocket lifecycle ----------
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        handler = self.commands.get(data.get("command"))
        if handler is None:
            return
        await handler(self, data)

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))