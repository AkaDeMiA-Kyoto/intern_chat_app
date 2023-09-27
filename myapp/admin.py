from django.contrib import admin
from .models import CustomUser, Message

class MemberAdmin(admin.ModelAdmin):
    list_display = ("username",)
    prepopulated_fields = {'slug': ('username',),}

admin.site.register(CustomUser, MemberAdmin)

admin.site.register(Message)
