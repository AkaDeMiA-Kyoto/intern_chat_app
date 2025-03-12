from django.contrib import admin
from .models import CustomUser, TalkLog

admin.site.register(CustomUser)
admin.site.register(TalkLog)