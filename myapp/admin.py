from django.contrib import admin
<<<<<<< HEAD
from .models import User, Talk

admin.site.register(User)
admin.site.register(Talk)
=======
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Message

# CustomUserモデルを管理サイトに登録
User = get_user_model()
admin.site.register(User)

# Messageモデルを管理サイトに登録
admin.site.register(Message)
>>>>>>> 568a137c735e2253106d8e0a27f94eeb14bead04
