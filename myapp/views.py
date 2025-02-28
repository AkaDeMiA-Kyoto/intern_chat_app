from django.shortcuts import redirect, render
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView

from .models import CustomUser
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

#from django.contrib.auth import authenticate #Djangoの認証システム]
#from django.contrib.auth.decorators import login_required



class IndexView(TemplateView):
    template_name = "myapp/index.html"
#def index(request): #requestはウェブサーバー⇀wsgiの流れで送られてきたrequestオブジェクト
    #return render(request, "myapp/index.html")

class SignupView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = "myapp/signup.html"
    success_url = reverse_lazy("index")

#def signup_view(request):
    # if request.method == 'POST':
    #     form = SignUpForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('index')
    # else:
    #     form = SignUpForm()
    # return render(request, 'myapp/signup.html', {'form': form})


class ChatLoginView(LoginView):
    template_name = "myapp/login.html"
    form_class = LoginForm
    # def post(self, request, *args, **kwargs):
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')

    #     user = authenticate(request, username=username,password=password)

    #     if user is not None:
    #         return super().post(request, *args, **kwargs)
    #     else:
    #         if not username or not password:
    #             error_massage = "ユーザー名とパスワードを入力してください。"
    #         else:
    #             error_massage = "ユーザー名またはパスワードが間違っています。"

    #         return render(request, self.template_name, {"error_message": error_massage})

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

class Setting(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/setting.html'

#ユーザー名変更するやつ
class UsernameChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["username"]
    template_name = 'myapp/username_change.html'
    success_url = reverse_lazy('setting')

    def get_object(self):
        return self.request.user #現在ログインしているユーザーの取得

#e-mail変更するやつ
class EmailChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["email"]
    template_name = 'myapp/email_change.html'
    success_url = reverse_lazy('setting')

    def get_object(self):
        return  self.request.user
    
#アイコン変更するやつ
class ImageChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields =["image"]
    template_name = 'myapp/image_change.html'
    success_url = reverse_lazy('setting')

    def get_object(self):
        return self.request.user  


#パスワード変更するやつ
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('password_change_done')
    template_name = 'myapp/password_change.html'
    login_url = reverse_lazy('index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "password_change"
        return context
    
class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'myapp/password_change_done.html'