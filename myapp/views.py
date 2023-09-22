from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.views.generic.edit import CreateView
from .models import CustomUser
from django.urls import reverse_lazy
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from .models import Talk
from django.shortcuts import get_object_or_404
from .forms import MessageForm
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import LogoutView
from .forms import IconUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    return render(request, "myapp/signup.html")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # ログイン成功後の処理
            return redirect('friends')  
    else:
        form = LoginForm()
    return render(request, "myapp/login.html", {'form': form})

def friends(request):
    # ユーザー一覧を取得し、各ユーザーの最新のトーク情報をフェッチ
    users = CustomUser.objects.all()
    for user in users:
        latest_talk = Talk.objects.filter(sender=user).order_by('-timestamp').first()
        user.latest_talk = latest_talk

    # ユーザー一覧を最新のトーク情報でソート
    sorted_users = sorted(users, key=lambda u: u.latest_talk.timestamp if u.latest_talk else timezone.now(), reverse=True)

    return render(request, "myapp/friends.html", {'users': sorted_users})
def talk_room(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # トークルーム内のメッセージをクエリ
    messages = Talk.objects.filter(
        (Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user))
    )

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            sender = request.user
            receiver = user  # メッセージの受信者は表示しているユーザー
            message_text = message_form.cleaned_data['message']

            # メッセージを保存
            Talk.objects.create(message=message_text, sender=sender, receiver=receiver)
            return redirect('talk_room', user_id=user_id)  # トークルームにリダイレクト
    else:
        message_form = MessageForm()

    return render(request, "myapp/talk_room.html", {'user': user, 'message_form': message_form, 'messages': messages})
def setting(request):
    return render(request, "myapp/setting.html")

def change_username(request):
    if request.method == 'POST':
        # ユーザー名を変更するロジックを実行
        new_username = request.POST['new_username']
        request.user.username = new_username
        request.user.save()
        return redirect('finish')  # ユーザー名の変更が成功した場合、'finish' ページにリダイレクト

    return render(request, 'myapp/username.html')

def change_email(request):
    if request.method == 'POST':
        new_email = request.POST['new_email']
        request.user.email = new_email
        request.user.save()

        return('finish')
    
    return render(request, 'myapp/email.html')

def change_icon(request):
    if request.method == 'POST':
        form = IconUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_icon = form.cleaned_data['new_icon']

            # アイコン画像の保存
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(new_icon.name, new_icon)

            # ユーザーモデルに新しいファイルパスを設定
            request.user.iamge = filename
            request.user.save()

            return redirect('finish')
    else:
        form = IconUploadForm()

    return render(request, 'myapp/icon.html', {'form': form})


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'myapp/password.html'  # テンプレート名
    success_url = reverse_lazy('finish')  # パスワード変更完了後のリダイレクト先

    def form_valid(self, form):
        # フォームが有効な場合の処理
        # パスワード変更を行います
        form.save()
        return super().form_valid(form)

class SignUpView(CreateView):
    template_name="myapp/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('index')

class loginview(LoginView):
    template_name="myapp/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('friends')
    
def finish(request):
    return render(request, "myapp/finish.html")

class logoutview(LogoutView):
    next_page = reverse_lazy('login_view')  # ログアウト後にリダイレクトするページを指定

    def dispatch(self, request, *args, **kwargs):
        # ログアウト処理を行い、指定したページにリダイレクトする
        response = super().dispatch(request, *args, **kwargs)
        return redirect(self.next_page)

