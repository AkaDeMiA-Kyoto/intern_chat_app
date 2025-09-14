from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Message

# CustomUserモデルを管理サイトに登録
User = get_user_model()
admin.site.register(User)

# Messageモデルを管理サイトに登録
admin.site.register(Message)