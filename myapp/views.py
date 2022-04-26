from django.shortcuts import redirect, render


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

def setting_username(request):
    return render(request, "myapp/setting_username.html")

def setting_mailaddress(request):
    return render(request, "myapp/setting_mailaddress.html")

def setting_icon(request):
    return render(request, "myapp/setting_icon.html")

def setting_password(request):
    return render(request, "myapp/setting_password.html")

def setting_username_completed(request):
    return render(request, "myapp/setting_username_completed.html")

def setting_mailaddress_completed(request):
    return render(request, "myapp/setting_mailaddress_completed.html")

def setting_icon_completed(request):
    return render(request, "myapp/setting_icon_completed.html")

def setting_password_completed(request):
    return render(request, "myapp/setting_password_completed.html")
