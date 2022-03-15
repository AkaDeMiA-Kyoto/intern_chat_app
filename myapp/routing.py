from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/talk_room/[\d]*/[\d]*',consumers.TalkConsumer.as_asgi())
]