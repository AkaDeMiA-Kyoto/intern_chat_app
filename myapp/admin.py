from django.contrib import admin

# Register your models here.

from .models import  Message

# admin.site.register(CustomUser)
admin.site.register(Message)
