from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/myapp/<int:id>/', consumers.ChatConsumer.as_asgi()),
]