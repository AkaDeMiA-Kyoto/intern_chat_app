from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from .forms import LoginForm

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form':form})

class LoginView(LoginView):
    template_name = 'myapp/login.html'
    authentication_form = LoginForm

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
