from django.contrib import admin
from .models import CustomUser
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=["id","username","email"]
    list_filter=["username"]
    search_fields=["username"]
    ordering=["id"]
    list_per_page=30
    list_editable=["username"]
    readonly_fields=["email"]
    exclude=["password"]
    fieldsets=[
        ("変更不可",{"fields":["email"]}),
        ("変更不可",{"fields":["username"]}),
    ]

admin.site.register(CustomUser,UserAdmin)