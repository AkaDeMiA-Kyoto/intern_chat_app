from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, path


def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("userが保存されました")
            return redirect("index")
        else:
            print("userに誤りがあります")
            return render(request, "myapp/signup.html", {"form": form})

    return render(request, "myapp/signup.html")


from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = "myapp/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("friends")

    def get_success_url(self):
        return self.success_url


def friends(request):
    return render(request, "myapp/friends.html")


def talk_room(request):
    return render(request, "myapp/talk_room.html")


def setting(request):
    return render(request, "myapp/setting.html")
