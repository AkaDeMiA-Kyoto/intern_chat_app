from django.contrib import admin
from .models import CustomUser, Friends, Message
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Friends)
admin.site.register(Message)