from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate #Djangoの認証システム
from .models import CustomUser




def index(request): #requestはウェブサーバー⇀wsgiの流れで送られてきたrequestオブジェクト
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

#def friends(request):
   # return render(request, "myapp/friends.html")

#友達リスト情報取得用関数
def getFriendsList(username):
    """
    指定したユーザーの友達リストを取得
    :param:ユーザー名
    :return:ユーザー名の友達リスト
    """
    try:
        user = CustomUser.objects.get(username=username)
        friends = list(user.user_friends.all()) #user_friendsはrelated_name="user_friends"の逆参照フィールド
        return friends
    except CustomUser.DoesNotExist:
        return []


def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

