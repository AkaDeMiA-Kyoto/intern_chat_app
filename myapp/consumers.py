import json
from typing import Any

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.forms.utils import ErrorDict
from django.core.exceptions import ObjectDoesNotExist

from .forms import TalkForm
from .models import Talk, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print("Connected:", self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]
        user_id = text_data_json["user_id"]

        if not message.strip() or self.user is None or user_id is None:
            return await self.send(json.dumps({"error": "通信に失敗しました"}))
        result: dict[str, Any] = await save_talk(
            talk_from=self.user, talk_to_id=user_id, talk=message
        )

        if "error" in result.keys():
            return await self.send(json.dumps({"error": result["error"]}))

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": result["message"]}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))


@database_sync_to_async
def save_talk(talk_from: User, talk_to_id: int, talk) -> dict:
    result = {}

    try:
        talk_to = User.objects.get(pk=talk_to_id)
    except ObjectDoesNotExist:
        result["error"] = ErrorDict({"get_talk_to": "指定されたユーザーがいません"})
        return result
    except Exception:
        result["error"] = ErrorDict({"get_talk_to": "送信に失敗しました"})
        return result

    new_talk = Talk(talk_from=talk_from, talk_to=talk_to)
    talk = TalkForm(data={"talk": talk}, instance=new_talk)

    if talk.is_valid():
        talk_instance = talk.save()
        result["message"] = {
            "talk": talk_instance.talk,
            "message_from": talk_from.username,
            "message_to": talk_to.username,
        }
    else:
        result["error"] = talk.errors

    return result
