from django.contrib import admin
from .models import CustomUser, TalkRoomModel, MessageModel

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(TalkRoomModel)
admin.site.register(MessageModel)
