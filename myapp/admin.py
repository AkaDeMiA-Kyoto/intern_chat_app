from django.contrib import admin

from .models import CustomUser, Friend, Talk, Message

admin.site.register(CustomUser)
admin.site.register(Friend)
admin.site.register(Talk)
admin.site.register(Message)
# Register your models here.
