from django.contrib import admin
from .models import CustomUser, Talk

admin.site.register(CustomUser)
admin.site.register(Talk)
# Register your models here.
