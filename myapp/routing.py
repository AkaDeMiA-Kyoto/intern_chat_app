from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/talk_room/(?P<room_id1>[\d]*)/(?P<room_id2>[\d]*)',consumers.TalkConsumer.as_asgi())
]