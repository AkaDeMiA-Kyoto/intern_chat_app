from django.contrib import admin
from .models import CustomUser
from .models import talk
admin.site.register(CustomUser)
admin.site.register(talk)