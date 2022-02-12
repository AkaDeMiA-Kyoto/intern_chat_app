from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/talk_room/<partner>', consumers.ChatConsumer.as_asgi()),
]
