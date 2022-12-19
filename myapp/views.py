from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from . import forms
from .models import MyUser, ChatContent
from django.db.models import Q

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            image = form.cleaned_data.get('img')
            user = authenticate(username=username, password=raw_password, img = image)
            login(request, user)
            return redirect('index')
        else:
            return render(request, "myapp/signup.html", {'form': form})
    else:
        form = forms.SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

class MyLogin(LoginView):
    form_class = forms.LoginForm
    template_name = "myapp/login.html" 


def friends(request):
    friends = MyUser.objects.all()
    context = {
        'friends': friends
    }
    return render(request, "myapp/friends.html", context)

def talk_room(request, username):
    user = request.user
    friend = MyUser.objects.get(username=username)
    if request.method == "POST":
        print(request.POST.get("content"))
        ChatContent.objects.create(
            send_to=friend,
            send_from=user,
            chat_content = request.POST.get("content")
        )
    chat_contents = ChatContent.objects.filter(
        Q(send_to=user, send_from=friend) |
        Q(send_to=friend, send_from=user)
    )
    context = {
        "friend": friend,
        "chat_contents": chat_contents
    }
    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")
