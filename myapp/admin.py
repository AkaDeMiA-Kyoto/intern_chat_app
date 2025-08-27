from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Message

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Message, admin.ModelAdmin)
# Register your models here.
