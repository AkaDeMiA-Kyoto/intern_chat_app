from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Talk
admin.site.register(CustomUser)
admin.site.register(Talk)
