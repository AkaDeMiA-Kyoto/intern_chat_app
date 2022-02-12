import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User, Message
from channels.db import database_sync_to_async

@database_sync_to_async
def get_id(person_name):
    return User.objects.get(username=person_name).unique_id

class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_id(self, person_name):
        return User.objects.get(username=person_name).unique_id

    async def connect(self):
        self.partner = self.scope['url_route']['kwargs']['partner']
        partner_id = await self.get_id(self.partner)
        user_id = await self.get_id(self.scope['user'])

        if(user_id < partner_id):
            group_name = str(partner_id) + str(user_id)
        else:
            group_name =str(user_id) + str(partner_id)

        # self.room_group_name = 'chat_%s' % self.partner
        self.room_group_name = group_name

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

    @database_sync_to_async
    def save_message(self, text_data_json):
        print("before save?2")
        data = eval(text_data_json)
        # message = Message(
        #     sender = data['sender'], \
        #     receiver = data['receiver'], \
        #     contents = data['message']
        # )
        print("before save?")
        Message.objects.create(
            sender = data['sender'], \
            receiver = data['receiver'], \
            contents = data['message']
        )
        print("save?")


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("W to G")
        await self.save_message(text_data)
        print("W to G after")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data_json['message'],
                'sender': text_data_json['sender'],
                'receiver': text_data_json['receiver']
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'receiver': event['receiver']
        }))