from django.contrib import admin
from .models import CustomUser, Room, Message

# Register your models here.
admin.site.register(CustomUser) #管理者サイトでUserモデルを見れるようにする
admin.site.register(Room) 
admin.site.register(Message)