from django.contrib import admin
from myapp.models import Message, Talker

admin.site.register(Talker)
admin.site.register(Message)

