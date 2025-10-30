import json
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.serializers import MessageSerializer
from .models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.username = self.scope["session"].get("username", "Guest")

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        last_msgs = [msg async for msg in Message.objects.filter(
            room_name=self.room_name).order_by("-timestamp")[:20]]

        for msg in reversed(last_msgs):
            await self.send(text_data=json.dumps(MessageSerializer(msg).data))

    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get("message", "").strip()
        if not message_text:
            return

        msg_obj = await sync_to_async(Message.objects.create)(room_name = self.room_name,
        username = self.username,
        message=message_text)
        message = msg_obj.to_dict()
        await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'message': message})

    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))