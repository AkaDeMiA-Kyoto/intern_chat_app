import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

Profile = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_id = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'chat'
        print(self.room_group_name)
        await self.channel_layer.group_add(  # グループにチャンネルを追加
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(  # グループからチャンネルを削除
            self.room_group_name,
            self.channel_name,
        )
        await self.close()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = await self.createMessage(message)
        user = self.scope["user"].username
        receiver = await database_sync_to_async(self.get_receiver)()
        await self.channel_layer.group_send(  # 指定グループにメッセージを送信する
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'receiver':receiver,
                'sender':sender,
                'user':user
            }
        )


    async def chat_message(self, event):
        message = event['message']
        receiver = event['receiver']
        sender = event['sender']
        user = event['user']
        await self.send(text_data=json.dumps({
            'type':'chat_message',
            'message':message,
            'receiver':receiver,
            'sender':sender,
            'user':user
        }))

    
    def get_receiver(self):
        return Profile.objects.get(pk=self.scope['url_route']['kwargs']['pk']).username


    @database_sync_to_async
    def createMessage(self, message):
        message_obj = Message.objects.create(
            sender = self.scope["user"],
            receiver = Profile.objects.get(pk=self.scope['url_route']['kwargs']['pk']),
            content = message,
        )
        return message_obj.sender.username

    