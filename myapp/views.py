from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import CustomUserCreationForm,CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    if request.method == "POST":
        print(request.FILES,request.POST)
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("userが保存されました")
            return redirect("index")
        else:
            print("userに誤りがあります",form.errors)
            return render(request, "myapp/signup.html", {"form": form})

    return render(request, "myapp/signup.html")


from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = "myapp/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("friends")
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return self.success_url

@login_required
def friends(request):
    users = CustomUser.objects.all()
    
    return render(request, "myapp/friends.html",{"users": users})

@login_required
def talk_room(request):
    return render(request, "myapp/talk_room.html")

@login_required
def setting(request):
    return render(request, "myapp/setting.html")
