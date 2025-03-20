from django.contrib import admin

from .models import CustomUser, Talk #, Friends
# Register your models here.
admin.site.register(CustomUser)

class TalkAdmin(admin.ModelAdmin):
    list_display=('send_user','recieve_user','talk_at','content')

admin.site.register(Talk, TalkAdmin)

# class FriendsAdmin(admin.ModelAdmin):
#     list_display=('pk','user','friends',)

#admin.site.register(Friends,FriendsAdmin)

