from django.contrib import admin

from .models import CustomUser, Chat

admin.site.register(CustomUser)
admin.site.register(Chat)

# Register your models here.
