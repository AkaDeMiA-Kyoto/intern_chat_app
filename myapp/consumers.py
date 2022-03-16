import json
from datetime import date,datetime
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import TalkModel,User

def datetime_dafault(o):
    if isinstance(o,(datetime,date)):
        return o.isoformat()

class TalkConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id1']+'-'+self.scope['url_route']['kwargs']['room_id2']
        self.room_group_name = 'talk_%s'%self.room_name

        #Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self,close_code):
        #Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    #Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        friend_id = text_data_json['friend_id']
        await self.createTalk(text_data_json)
        time = datetime.now()
        time_json = json.dumps(time,default=datetime_dafault)

        #Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'talk_message',
                'message': message,
                'friend_id': friend_id,
                'time': time_json
            }
        )
    
    #Receive message from room group
    async def talk_message(self,event):
        message = event['message']
        sender = str(self.scope['user'])
        time = event['time']
        
        #Send message to WebSocket
        await self.send(text_data = json.dumps({
            'message':message,
            'sender':sender,
            'time':time
        }))
    
    @database_sync_to_async
    def createTalk(self,event):
        friend_id = event['friend_id']
        friend = User.objects.get(id=friend_id)
        TalkModel.objects.create(
            sender = self.scope['user'],
            talkname = friend,
            content = event['message'],
            pub_date = datetime.now(),
        )
    