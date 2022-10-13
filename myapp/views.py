from django.shortcuts import redirect, render
from . import forms
from .models import MyUser, ChatContent
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, Subquery, OuterRef
from allauth.account.models import EmailAddress
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy


def index(request):
    # すでにログイン済みのユーザーがインデックスに訪れた場合、リダイレクトさせる
    if request.user.is_authenticated:
        return redirect('myapp:friends')
    return render(request, "myapp/index.html")


@login_required
def friends(request):
    if 'name' in request.GET:
        name = request.GET.get('name')
        # ユーザー名またはメールアドレスで部分一致検索をかける
        friend_list = MyUser.objects.prefetch_related('message_sent', 'message_was_sent').filter(Q(username__contains=name) | Q(email__contains=name)).order_by('pub_date')
        bottom_message = '（条件に当てはまるユーザーは以上です）'
    else:
        name = ''
        # N+1問題を回避するため、あらかじめそのユーザーが送信したメッセージを取得しておく
        friend_list = MyUser.objects.prefetch_related('message_sent', 'message_was_sent').all().order_by('pub_date')
        bottom_message = '（これ以上登録済みのユーザーはいません）'
    # 最新のトークデータを取得する部分をannotateにより実装
    id1 = request.user.id
    latest_chat_content = ChatContent.objects.filter(Q(send_from__id=id1, send_to__id=OuterRef('pk')) | Q(send_from__id=OuterRef('pk'), send_to__id=id1)).order_by('-pub_date')
    # OuterRefを使うことで、Subqueryの外側であるfriend_listのフィールドにアクセスできる
    # annotateは新しいクエリセットを返してくるので、受け取る必要がある
    friend_list = friend_list.annotate(latest_message=Subquery(latest_chat_content.values('chat_content')[:1]))  # [:1]とすることでもし会話がなくてもエラー(list index out of range)にならないようにする
    context = {
        'friends': friend_list,
        'name': name,
        'bottom_message': bottom_message,
    }
    return render(request, "myapp/friends.html", context)


@login_required
def talk_room(request, friend_id):
    if request.method == 'POST':
        form = forms.ChatForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # フォームの情報をコミットせずに保存（追加情報を登録するため）
            post.pub_date = timezone.now()  # 登録日時の設定
            post.send_to = MyUser.objects.get(pk=friend_id)  # 誰に送るか
            post.send_from = request.user  # 誰から送られるか
            post.save()
            return redirect('myapp:talk_room', friend_id)
    else:
        # select_relatedしておくことで、テンプレートでfor文を回すたびに送信者名などを取得するクエリが発行されないようにする
        contents = ChatContent.objects.select_related('send_from', 'send_to').filter(Q(send_from__id=request.user.id, send_to__id=friend_id) | Q(send_from__id=friend_id, send_to__id=request.user.id)).order_by('pub_date')
        form = forms.ChatForm()
        context = {
            'contents': contents,
            'id': friend_id,
            'form': form,
            'partner': MyUser.objects.get(pk=friend_id),
        }
        return render(request, "myapp/talk_room.html", context)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")


@login_required
def name_change(request):
    if request.method == 'POST':
        form = forms.NameChangeForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data["username"]
            user_obj = MyUser.objects.get(pk=request.user.id)
            user_obj.username = new_name
            user_obj.save()
            return redirect('myapp:setting')
    else:
        form = forms.NameChangeForm()  # postでない（すなわちget）の場合はからのフォームを作って渡す
    context = {
        'form': form,
    }
    return render(request, "myapp/name_change.html", context)


@login_required
def email_change(request):
    if request.method == 'POST':
        form = forms.EmailChangeForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data["email"]
            EmailAddress.objects.create(user=request.user, email=new_email, primary=False)
            # allauthのメールアドレスモデルに登録（MyUserモデルに反映するのは確認後）
            return redirect('myapp:setting')
    else:
        form = forms.EmailChangeForm()
    context = {
        'form': form,
    }
    return render(request, "myapp/email_change.html", context)


@login_required
def icon_change(request):
    if request.method == 'POST':
        form = forms.IconChangeForm(request.POST, request.FILES)
        if form.is_valid():
            new_img = form.cleaned_data["img"]
            user_obj = MyUser.objects.get(pk=request.user.id)
            user_obj.img = new_img
            user_obj.save()
            return redirect('myapp:setting')
    else:
        form = forms.IconChangeForm()
    context = {
        'form': form,
    }
    return render(request, "myapp/icon_change.html", context)
