from django.contrib import admin
from .models import Signup, Message

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    fields=["username","email","password1","password2","img",]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields=["message","sender","recipient","sended_at","id",]
    readonly_fields=["sended_at","id",]