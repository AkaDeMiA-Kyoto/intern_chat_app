from django.contrib import admin

from .models import CustomUser
from .models import Message

admin.site.register(CustomUser)
admin.site.register(Message)
