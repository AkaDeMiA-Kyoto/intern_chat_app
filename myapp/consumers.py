import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Talk, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'chat_%s' % self.id
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        t_user = text_data_json['t_user']
        f_user = text_data_json['f_user']

        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                't_user': t_user,
                'f_user': f_user,
            }
        )
        await self.save_message(t_user, f_user, message)

    # Receive message from room group
    async def chat_message(self, event):
        print(3)
        message = event['message']
        t_user = event['t_user']
        f_user = event['f_user']
    
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, t_user, f_user, message):
        """ データベースに保存し、そのidを返す """
        print(t_user)
        print(f_user)
        print(message)    
 
        t_user = User.objects.get(id=t_user)
        f_user = User.objects.get(id=f_user)
        talk = Talk(f_user=f_user, t_user=t_user, content=message)
        talk.save()