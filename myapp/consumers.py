import json 
#from channels.generic.websocket import WebsocketConsumer
#from asgiref.sync import async_to_sync #非同期関数を同期的に実行する際に使用する。
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from datetime import date, datetime

from myapp.models import Talk,CustomUser

# ChatConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class ChatConsumer(AsyncWebsocketConsumer):

    # WebSocket接続時の処理
    async def connect(self):
        # グループに参加
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # WebSocket接続を受け入れます。
        # ・connect()でaccept()を呼び出さないと、接続は拒否されて閉じられます。
        # 　たとえば、要求しているユーザーが要求されたアクションを実行する権限を持っていないために、接続を拒否したい場合があります。
        # 　接続を受け入れる場合は、connect()の最後のアクションとしてaccept()を呼び出します。
        await self.accept()
        
     # WebSocket切断時の処理
    async def disconnect(self, close_code):
        # グループから離脱
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    async def receive(self, text_data):
        # 受信データをJSONデータに復元
        text_data_json = json.loads(text_data)
        # メッセージの取り出し
        message = text_data_json['message']
        user_id = int(text_data_json['user_id'])
        friend_id = int(text_data_json['friend_id'])

        # データベースに保存、各種値の取得
        user = await self.get_user(user_id)
        friend = await self.get_user(friend_id)
        talk = await self.save_message(user, friend, message)
        username = '＞' + user.username
        time = talk.time

        #datetimeをフォーマット
        now_time = f'{time:%m/%d %H:%M}'

        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', 
                'message': message,
                'username': username,
                'time': now_time,
                'user_id': str(user_id),
                'room_id': self.room_id,
            }
        )

    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']
        user_id = event['user_id']
        room_id = event['room_id']

        # WebSocketにメッセージを送信します。
        # （送信されたメッセージは、ブラウザ側のJavaScript関数のsocketChat.onmessage()で受信処理されます）
        # JSONデータにエンコードして送ります。
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time':time,
            'user_id': user_id,
            'room_id': room_id,
        }))
    
    # DB操作を伴う処理を含んだメソッド
    @database_sync_to_async
    def save_message(self, user, friend, message):
        """ データベースに保存し、そのidを返す """
        talk = Talk.objects.create(talk_from=user, talk_to=friend, talk=message)
        return talk
    
    @database_sync_to_async
    def get_user(self, user_id:int):
        """ userの取得 """
        return CustomUser.objects.get(id=user_id)

    


    