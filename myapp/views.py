from django.shortcuts import redirect, render

from .models import CustomUser
# 会員登録
from .forms import CustomSignUpForm
# ログイン
from django.views import generic
# 友だち表示, トークルーム
from django.contrib.auth.decorators import login_required
from .models import Message
# トークルーム
from django.db.models import Q, Max
from .forms import MessageForm
# 設定
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LogoutView
from django.urls import reverse_lazy
from .forms import UserUpdateForm

class IndexView(generic.TemplateView):
    def get_template_names(self):
        template_name = "index.html"
        return [template_name]

class SignUpView(generic.TemplateView):
    form_class = CustomSignUpForm

    def get(self, request, *args, **kwargs):
        print('get')
        form = CustomSignUpForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CustomSignUpForm(request.POST, request.FILES)
        # for _ in range(10):
            # print('post') conmout
        if form.is_valid():
            # print('no errors') comout
            pass
        else:
            # print('some error occurs') comout
            return render(request, 'signup.html', {'form':form})

@login_required
def friends(request):
    user = request.user
    # 土佐さんありがとうございました！
    friends = CustomUser.objects.raw(
        f"""
        SELECT *
        FROM (
            SELECT
            u.id as id,
            u.username as username,
            row_number() over (
                partition by
                u.id
                order by
                t.sendtime desc
            ) rownum,
            t.content as content
            FROM myapp_customuser u 
            LEFT OUTER JOIN myapp_message t 
                ON (u.id=t.sender_id OR u.id=t.receiver_id)
            WHERE (t.sender_id={user.id} OR t.receiver_id={user.id}) AND NOT u.id={user.id}
        ) f
        WHERE f.rownum=1;
        """)

    unknown_friends = CustomUser.objects.exclude(id=request.user.id).annotate(
        sender__sendtime__max=Max("sender__sendtime", filter=Q(sender__receiver=user)),
        receiver__sendtime__max=Max("receiver__sendtime", filter=Q(receiver__sender=user)),
    ).filter(sender__sendtime__max=None, receiver__sendtime__max=None).order_by("id")

    params = {
        "user":request.user.username,
        "header_title":"友だち",
        "title":"",
        "friends": friends,
        "unknown_friends": unknown_friends,
    }

    return render(request, "myapp/friends.html", params)

@login_required
def talk_room(request, your_id):
    # 送る側のユーザー
    me = request.user
    # 受け取る側のユーザー
    you = CustomUser.objects.get(id = your_id)

    data = Message.objects.select_related('sender', 'receiver').filter( Q(sender=me) | Q(receiver=me) ).filter( Q(sender=you) | Q(receiver=you) ).order_by("sendtime")

    params = {
        "sender":me,
        "receiver":you,
        "title":"",
        "form":MessageForm(),
        "data":data,
    }

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            newrecord = Message(
                sender = request.user,
                receiver = you,
                content = form.cleaned_data["content"],
            )
            newrecord.save()
    return render(request, "myapp/talk_room.html", params)

def setting(request):
    params = {
        "user":request.user,
        "header_title":"設定",
    }
    return render(request, "myapp/setting.html", params)

def change_setting(request, change_command, your_id):
    obj = CustomUser.objects.get(id=your_id)
    params = {
        "user":request.user,
        "header_title":"",
        "change_command":"",
        "isform":True,
        "form":UserUpdateForm(),
    }

    if change_command == "change_username":
        params["header_title"] = "ユーザ名変更"
    elif change_command == "change_email":
        params["header_title"] = "メールアドレス変更"
    elif change_command == "change_image":
        params["header_title"] = "アイコン変更"
    params["change_command"] = params["header_title"]

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            print("フォームは有効です")
            if change_command == "change_username":
                obj.username = form.cleaned_data["username"]
            elif change_command == "change_email":
                obj.email = form.cleaned_data["email"]
            elif change_command == "change_image":
                obj.image = form.cleaned_data["image"]
            obj.save()
            params["isform"] = False
            return redirect(to="/change_setting_done/" + str(change_command))
        else:
            print("フォームは有効ではありません")
    return render(request, "myapp/change_setting.html", params)

def change_setting_done(request, change_command):
    params = {
        "change_command":"",
    }
    if change_command == "change_username":
        params["change_command"] = "ユーザ名の変更"
    elif change_command == "change_email":
        params["change_command"] = "Eメールアドレスの変更"
    elif change_command == "change_image":
        params["change_command"] = "アイコンの変更"
    return render(request, "myapp/change_setting_done.html", params)

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    '''パスワード変更ビュー'''
    success_url = reverse_lazy('password_change_done')
    template_name = 'myapp/change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "password_change"
        return context

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    '''パスワード変更完了'''
    template_name = 'myapp/change_password_done.html'

class Logout(LogoutView):
    success_url = reverse_lazy("index")