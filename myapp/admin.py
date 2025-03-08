from django.contrib import admin
from .models import Signup

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    fields=["username","email","password1","password2","img"]