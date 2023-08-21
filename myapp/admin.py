from django.contrib import admin

from .models import CustomUser, TalkContent

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(TalkContent)
