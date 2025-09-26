<<<<<<< HEAD
import operator

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import (
    ImageSettingForm,
    LoginForm,
    MailSettingForm,
    PasswordChangeForm,
    SignUpForm,
    TalkForm,
    UserNameSettingForm,
)
from .models import Talk

from django.contrib import messages
from django.urls import reverse
from .models import OTPCode
from django.core.mail import send_mail
from .forms import OTPVerificationForm
from datetime import datetime


User = get_user_model()

=======
from django.shortcuts import redirect, render, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from .models import Message
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
>>>>>>> 568a137c735e2253106d8e0a27f94eeb14bead04

def index(request):
    return render(request, "myapp/index.html")


def signup_view(request):
<<<<<<< HEAD
    if request.method == "GET":
        form = SignUpForm()
        error_message = ''
    elif request.method == "POST":
        # 画像ファイルをformに入れた状態で使いたい時はformに"request.FILES"を加える。
        # request.POST だけではNoneが入る。
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # モデルフォームはformの値をmodelsにそのまま格納できるsave()メソッドがあるので便利。
            form.save()
            # フォームから"username"を読み取る
            username = form.cleaned_data.get("username")
            # フォームから"password1"を読み取る
            password = form.cleaned_data.get("password1")
            # 認証情報のセットを検証するには authenticate() を利用してください。
            # このメソッドは認証情報をキーワード引数として受け取ります。
            # 検証する対象はデフォルトでは username と password であり
            # その組み合わせを個々の 認証バックエンド に対して問い合わせ、認証バックエンドで認証情報が有効とされれば
            # User オブジェクトを返します。もしいずれの認証バックエンドでも認証情報が有効と判定されなければ PermissionDenied が送出され、None が返されます。
            # (公式ドキュメントより)
            # つまり、autenticateメソッドは"username"と"password"を受け取り、その組み合わせが存在すれば
            # そのUserを返し、不正であれば"None"を返します。
            user = authenticate(username=username, password=password)
            if user is not None:
                # あるユーザーをログインさせる場合は、login() を利用してください。この関数は HttpRequest オブジェクトと User オブジェクトを受け取ります。
                # ここでのUserは認証バックエンド属性を持ってる必要がある。
                # authenticate()が返すUserはuser.backendを持つので連携可能。
                login(request, user)
            return redirect("/")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

            

    context = {
        "form": form,
    }
    return render(request, "myapp/signup.html", context)


class Login(LoginView):
    """ログインページ
    GETの時は指定されたformを指定したテンプレートに表示
    POSTの時はloginを試みる。→成功すればsettingのLOGIN_REDIRECT_URLで指定されたURLに飛ぶ
    """

    authentication_form = LoginForm
    template_name = "myapp/login.html"

    def form_valid(self, form):
        """
        パスワード認証が成功した後に実行されるメソッド。
        """
        user = form.get_user()
        if user.is_authenticated:
            login(self.request, user)
            # 1. パスコードを生成または取得する
            otp_code, created = OTPCode.objects.get_or_create(user=user)
            if not created:
                # 既存のパスコードを更新するロジック
                otp_code.passcode = otp_code._meta.get_field('passcode').get_default()
                otp_code.created_at = datetime.now()
                otp_code.save()

            # 2. パスコードをメールで送信する
            send_mail(
                '2段階認証パスコード',
                f'あなたのパスコードは {otp_code.passcode} です。',
                'from@example.com',
                [user.email],
            )

            # 3. 2段階認証用のビューにリダイレクトする
            return redirect(reverse('verify_otp')) # 'verify_otp'はurls.pyで定義したURL名

        # パスワード認証に失敗した場合の処理（デフォルトの挙動を継承）
        return super().form_valid(form)


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""


@login_required
def friends(request):
    user = request.user
    friends = User.objects.exclude(id=user.id)

    query = request.GET.get('q')
=======
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = SignUpForm()

    return render(request, 'myapp/signup.html', {'form': form})

class login_view(LoginView):
    # ログイン画面のテンプレートを指定
    template_name = 'myapp/login.html'

    # ログイン成功後のリダイレクト先URL名を指定
    authentication_form = AuthenticationForm

class friends(LoginRequiredMixin, ListView):
    template_name = 'myapp/friends.html'
    model = get_user_model()
    context_object_name = 'users'

    def get_queryset(self):
        current_user = self.request.user
        all_users = get_user_model().objects.exclude(pk=current_user.pk).exclude(is_staff=True)
        
        user_list = []
        talked_with = set()

        # 1. トークしたことのあるユーザーをリストアップ
        for user in all_users:
            latest_message = Message.objects.filter(
                (models.Q(sender=current_user, receiver=user) | models.Q(sender=user, receiver=current_user))
            ).order_by('-timestamp').first()

            if latest_message:
                user_list.append({
                    'user': user,
                    'latest_talk': latest_message.content,
                    'latest_talk_time': latest_message.timestamp,
                    'has_talked': True,
                })
                talked_with.add(user.pk)

        # 2. まだトークしていないユーザーをリストアップ
        untalked_users = all_users.exclude(pk__in=talked_with).order_by('-date_joined')
        for user in untalked_users:
            user_list.append({
                'user': user,
                'latest_talk': 'まだトークしていません',
                'latest_talk_time': user.date_joined,
                'has_talked': False,
            })

        # 3. トークしたことのあるユーザーを最新トーク時間でソート
        talked_users = sorted([u for u in user_list if u['has_talked']], key=lambda x: x['latest_talk_time'], reverse=True)
        untalked_users = [u for u in user_list if not u['has_talked']]

        return talked_users + untalked_users

class talk_room(LoginRequiredMixin, View):
    def get(self, request, username):
        # URLから渡されたusernameで相手ユーザーを取得
        talk_partner = get_object_or_404(get_user_model(), username=username)

        messages = Message.objects.filter(
            models.Q(sender=request.user, receiver=talk_partner) | models.Q(sender=talk_partner, receiver=request.user)
        ).order_by('timestamp')
        
        # ここにトーク履歴を取得するロジックを実装
        context = {
            'talk_partner': talk_partner,
            'messages': messages,
        }
        return render(request, 'myapp/talk_room.html', context)
    
    def post(self, request, username):
        talk_partner = get_object_or_404(get_user_model(), username=username)
        content = request.POST.get('content')
        
        if content:
            # 新しいメッセージをデータベースに保存
            Message.objects.create(
                sender=request.user,
                receiver=talk_partner,
                content=content
            )
        
        # 同じトークルームにリダイレクトして、画面を更新
        return redirect('talk_room', username=username)
>>>>>>> 568a137c735e2253106d8e0a27f94eeb14bead04

    if query:
        friends = friends.filter(username__icontains=query)

    # トーク情報とフレンド情報を含む info を作成
    info = []
    info_have_message = []
    info_have_no_message = []
    
    for friend in friends:
        # 最新のメッセージの取得
        latest_message = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
        ).order_by('time').last()

        if latest_message:
            info_have_message.append([friend, latest_message.talk, latest_message.time])
        else:
            info_have_no_message.append([friend, None, None])
    
    # 時間順に並び替え
    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)
    
    info.extend(info_have_message)
    info.extend(info_have_no_message)
    
    context = {
        "info": info,
    }
    return render(request, "myapp/friends.html", context)


@login_required
def talk_room(request, user_id):
    # ユーザ・友達をともにオブジェクトで取得
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    # 自分→友達、友達→自分のトークを全て取得
    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).order_by("time")
    # 送信form
    form = TalkForm()
    # メッセージ送信だろうが更新だろが、表示に必要なパラメーターは変わらないので、この時点でまとめて指定
    context = {
        "form": form,
        "talk": talk,
        "friend": friend,
    }

    # POST（メッセージ送信あり）
    if request.method == "POST":
        # 送信内容を取得
        new_talk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=new_talk)

        # 送信内容があった場合
        if form.is_valid():
            # 保存
            form.save()
            # 更新
            # このようなリダイレクト処理はPOSTのリクエストを初期化し、リクエストをGETに戻すことにより
            # 万一更新処理を連打されてもPOSTのままにさせない等の用途がある
            return redirect("talk_room", user_id)
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    # POSTでない（リダイレクトorただの更新）&POSTでも入力がない場合
    return render(request, "myapp/talk_room.html", context)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")

<<<<<<< HEAD

# setting以下のchange系の関数は
# request.methodが"GET"か"POST"かで明示的に分けています。
# これはformの送信があった時とそうで無いときを区別しています。


@login_required
def user_img_change(request):
    user = request.user
    if request.method == "GET":
        # モデルフォームには `instance=user` をつけることで user の情報が入った状態のフォームを参照できます。
        # 今回はユーザ情報の変更の関数が多いのでこれをよく使います。
        form = ImageSettingForm(instance=user)

    elif request.method == "POST":
        form = ImageSettingForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_img_change_done")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/user_img_change.html", context)


@login_required
def user_img_change_done(request):
    return render(request, "myapp/user_img_change_done.html")


@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailSettingForm(instance=user)

    elif request.method == "POST":
        form = MailSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("mail_change_done")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/mail_change.html", context)


@login_required
def mail_change_done(request):
    return render(request, "myapp/mail_change_done.html")


@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)

    elif request.method == "POST":
        form = UserNameSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
        # バリデーションが通らなかった時の処理を記述
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/username_change.html", context)


@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")


class PasswordChange(PasswordChangeView):
    """Django標準パスワード変更ビュー

    Attributes:
        template_name: 表示するテンプレート
        success_url: 処理が成功した時のリダイレクト先
        form_class: パスワード変更フォーム
    """

    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "myapp/password_change.html"


class PasswordChangeDone(PasswordChangeDoneView):
    """Django標準パスワード変更後ビュー"""



@login_required
def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data.get('passcode')
            try:
                # ユーザーとパスコードの組み合わせを検証
                otp_code = OTPCode.objects.get(user=request.user, passcode=passcode)
                if otp_code.is_valid():
                    # 認証成功
                    login(request, request.user)
                    messages.success(request, '認証に成功しました。')
                    otp_code.delete() # パスコードを削除
                    return redirect(reverse('friends'))  # ログイン後のページにリダイレクト
                else:
                    messages.error(request, 'パスコードの有効期限が切れています。再度ログインしてください。')
            except OTPCode.DoesNotExist:
                messages.error(request, '無効なパスコードです。')
    else:
        form = OTPVerificationForm()
    return render(request, 'myapp/verify_otp.html', {'form': form})
=======
class username(LoginRequiredMixin, View):
    def get(self, request):
        # ユーザー名変更ページを表示
        return render(request, 'myapp/username.html')

    def post(self, request):
        new_username = request.POST.get('new_username')
        user = request.user

        if new_username:
            # 新しいユーザー名がすでに使われているか確認
            if user.__class__.objects.filter(username=new_username).exists():
                messages.error(request, 'このユーザー名はすでに使用されています。')
            else:
                user.username = new_username
                user.save()
                messages.success(request, 'ユーザー名を変更しました。')
                return redirect('username')

        return render(request, 'myapp/username.html')
    
class email(LoginRequiredMixin, View):
    def get(self, request):
        # メールアドレス変更ページを表示
        return render(request, 'myapp/email.html')

    def post(self, request):
        new_email = request.POST.get('new_email')
        user = request.user

        if new_email:
            # 1. メールアドレスの形式を検証
            try:
                validate_email(new_email)
            except ValidationError:
                messages.error(request, '無効なメールアドレスです。')
                return render(request, 'myapp/email.html')
                
            user.email = new_email
            user.save()
            messages.success(request, 'メールアドレスを変更しました。')
            return redirect('change_email')

        return render(request, 'myapp/email.html')
    
class icon(LoginRequiredMixin, View):
    def get(self, request):
        # アイコン変更ページを表示
        return render(request, 'myapp/icon.html')

    def post(self, request):
        new_icon = request.FILES.get('new_icon')
        user = request.user

        if new_icon:
            # 既存のアイコンを削除
            if user.image:
                user.image.delete(save=False)
            
            # 新しいアイコンをアップロード
            user.image = new_icon
            user.save()
            
            messages.success(request, 'アイコンを変更しました。')
            return redirect('icon')
        else:
            messages.error(request, 'ファイルが選択されていません。')

        return render(request, 'myapp/icon.html')
>>>>>>> 568a137c735e2253106d8e0a27f94eeb14bead04
