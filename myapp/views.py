from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm 



def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.POST:
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, "myapp/signup.html", context)

class login_view(LoginView):
    template_name = 'myapp/login.html'

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

