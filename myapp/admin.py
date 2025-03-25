from django.contrib import admin
from .models import Signup, Message

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    fields=["username","email","password1","password2","img"]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields=["message","sender","recipient","user1","user2","sended_at","id","last_sended_at",]
    readonly_fields=["sended_at","id","last_sended_at",]