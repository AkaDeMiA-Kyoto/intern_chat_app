from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate #Djangoの認証システム



def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})


class ChatLoginView(LoginView):
    template_name = "myapp/login.html"
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            return super().post(request, *args, **kwargs)
        else:
            if not username or not password:
                error_massage = "ユーザー名とパスワードを入力してください。"
            else:
                error_massage = "ユーザー名またはパスワードが間違っています。"

            return render(request, self.template_name, {"error_message": error_massage})

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

