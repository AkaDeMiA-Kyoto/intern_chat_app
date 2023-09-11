from django.shortcuts import redirect, render, get_object_or_404
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignupForm()
        error_message = ''
    elif request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("/")
        else:
            print(form.errors)
    context = {
        "form": form,
    }
    return render(request, "myapp/signup.html", context)

class Login(LoginView):
    authentication_form = LoginForm
    template_name = "myapp/login.html"

class Logout(LoginRequiredMixin, LogoutView):
    template_name = "myapp/login.html"

def friends(request):
    
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")
