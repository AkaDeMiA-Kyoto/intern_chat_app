from django.contrib import admin

from .models import CustomUser, Friends
# Register your models here.
admin.site.register(CustomUser)

class FriendsAdmin(admin.ModelAdmin):
    list_display=('pk','user','friends',)

admin.site.register(Friends,FriendsAdmin)