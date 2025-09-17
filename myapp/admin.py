from django.contrib import admin
from .models import CustomUser, Friend

admin.site.register(CustomUser)
admin.site.register(Friend)
