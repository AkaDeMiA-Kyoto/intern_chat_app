from re import A
from django.contrib import admin
from .models import TalkModel, User

# Register your models here.

admin.site.register(User)

admin.site.register(TalkModel)