from django.shortcuts import redirect, render, get_object_or_404
from .forms import CustomUserCreationForm, LoginForm, Username_UpdateForm, Email_UpdateForm, Img_UpdateForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import CustomUser, Room, Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Subquery, OuterRef, F



def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, "myapp/signup.html", {'form': form})

class login_view(LoginView):
    # settings.py で定義した AUTH_USER_MODEL に指定されたモデルクラスのインスタンスに対してログイン
    # デフォルトはUserクラス
    template_name = 'myapp/login.html'
    authentication_form = LoginForm
    # ログイン時のフォームクラスの指定

class logout_view(LoginRequiredMixin, LogoutView):
    pass

def username_update(request):
    user = request.user

    if request.method == 'POST':
        # フォーム送信データを受け取る
        form = Username_UpdateForm(request.POST, request.FILES, instance=user) # ここで初期化と同時にバリデーションも行われる
        if form.is_valid(): # バリデーションを通過した（入力内容に問題がなかった）場合は form.is_valid が True になる
            # バリデーションを通過したデータは form.cleaned_data['<フィールド名>'] で取得
            form.save()
            return redirect('done_view')

    else:
        # POST メソッドでなかった場合は空のフォームを渡す
        form = Username_UpdateForm()

    # バリデーションが失敗した or POSTメソッドでなかった場合はこのフォーム画面を再度表示
    return render(request, 'myapp/username_update.html', {'form': form})

def email_update(request):
    user = request.user
    if request.method == 'POST':
        # フォーム送信データを受け取る
        form = Email_UpdateForm(request.POST, request.FILES, instance=user) # ここで初期化と同時にバリデーションも行われる
        if form.is_valid(): # バリデーションを通過した（入力内容に問題がなかった）場合は form.is_valid が True になる
            # バリデーションを通過したデータは form.cleaned_data['<フィールド名>'] で取得
            form.save()
            return redirect('done_view')

    else:
        # POST メソッドでなかった場合は空のフォームを渡す
        form = Email_UpdateForm()

    # バリデーションが失敗した or POSTメソッドでなかった場合はこのフォーム画面を再度表示
    return render(request, 'myapp/email_update.html', {'form': form})

def img_update(request):
    user = request.user
    if request.method == 'POST':
        # フォーム送信データを受け取る
        form = Img_UpdateForm(request.POST, request.FILES, instance=user) # ここで初期化と同時にバリデーションも行われる
        if form.is_valid(): # バリデーションを通過した（入力内容に問題がなかった）場合は form.is_valid が True になる
            # バリデーションを通過したデータは form.cleaned_data['<フィールド名>'] で取得
            form.save()
            return redirect('done_view')

    else:
        # POST メソッドでなかった場合は空のフォームを渡す
        form = Img_UpdateForm()

    # バリデーションが失敗した or POSTメソッドでなかった場合はこのフォーム画面を再度表示
    return render(request, 'myapp/img_update.html', {'form': form})

def update_done(request):
    return render(request, "myapp/update_done.html")


class password_update_view(LoginRequiredMixin, PasswordChangeView):
    template_name = 'myapp/password_update.html'
    success_url = 'password_update_done'

class password_update_done_view(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'myapp/password_update_done.html'



class FriendsListView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = 'myapp/friends.html'
    context_object_name = 'friends_list'

    def get_queryset(self):
        user = self.request.user

        # 1. 自分以外の全ユーザーを取得
        queryset = CustomUser.objects.exclude(pk=user.pk)

        # 2. 最新メッセージを取得するための、よりシンプルなサブクエリを定義
        #   - このサブクエリは、メインクエリの各ユーザー(OuterRef('pk'))と
        #     ログインユーザー(user)の両方が参加しているRoomに属する
        #     Messageを全て絞り込む。
        #   - そして、その中から作成日時が最新のものを1つだけ取得する。
        latest_message_subquery = Message.objects.filter(
            room__participants=user).filter(room__participants=OuterRef('pk')).order_by('-created_at')

        # 3. メインのクエリに最新メッセージの日時と内容をアノテーションする
        queryset = queryset.annotate(
            latest_message_time=Subquery(latest_message_subquery.values('created_at')[:1]),
            latest_message_content=Subquery(latest_message_subquery.values('content')[:1])
        )

        # 4. アノテーションした最新メッセージの日時で全体を並べ替える
        queryset = queryset.order_by(F('latest_message_time').desc(nulls_last=True))

        return queryset

    # def get_queryset(self):
    #     # get_querysetメソッドをオーバーライドして、メインのクエリをここで定義します。
    #     # ビューがどんなデータをデータベースから取得するかを決めるためのメソッド
        
    #     user = self.request.user

    #     queryset = CustomUser.objects.exclude(pk=user.pk)
    #     # 自分以外の全ユーザーを取得

    #     room_subquery = Room.objects.filter(Q(participants=user) & Q(participants=OuterRef('pk'))).order_by('-id')  # Room の id だけ取る
    #     # 1. 各ユーザー(OuterRef)とログインユーザー(user)が参加しているRoomを探す
    #     # Subquery(room_subquery.values('pk')[:1]) が複数返している
    #     # サブクエリが複数の Room を返すと、Django はエラーではなく空の結果を返すことがあります。
    #     # 最新の Room を 1件だけに絞るために order_by が必要です。
    #     # .order_by('-id') は Django ORM のメソッドで、クエリ結果を id の降順 に並べ替えるという意味
    #     # 先頭に - をつけると 降順（大きいものから小さいものへ）つけないと昇順（小さいものから大きいものへ）
    #     # メインクエリの各ユーザーを指す

    #     # 2. 上記で見つかったRoomの最新メッセージを取得するクエリ
    #     latest_message_subquery = Message.objects.filter(room=Subquery(room_subquery.values('pk')[:1])).order_by('-created_at')

    #     # 3. メインのクエリに最新メッセージの日時と内容を「アノテーション(メモ機能)」する
    #     queryset = queryset.annotate(
    #         # 最新メッセージの日時をquerysetの各オブジェクトに 'latest_message_time' という名前で追加
    #         latest_message_time=Subquery(latest_message_subquery.values('created_at')[:1]),
    #         # 最新メッセージの内容をquerysetの各オブジェクトに 'latest_message_content' という名前で追加
    #         latest_message_content=Subquery(latest_message_subquery.values('content')[:1]))

    #     # 4. アノテーションした最新メッセージの日時で全体を並べ替える
    #     # F() を使うと、「値そのもの」をデータベース上で扱えるようになる
    #     # .descは降順
    #     # メッセージがない相手は後ろに来るように、NULLS LASTを指定（NULL のデータは、最後（last）に持ってくる）
    #     queryset = queryset.order_by(F('latest_message_time').desc(nulls_last=True))

    #     return queryset

    # def get_context_data(self, **kwargs):
    #     # get_context_dataはテンプレートに渡す追加contextデータを定義するために使われる
    #     ctx = super().get_context_data(**kwargs)

    #     friends = ctx['object_list'] 

    #     latest_message_qs = Message.objects.filter(room=OuterRef('room')).order_by('-created_at')
    #     # 下がメインの問い合わせなので、下を先に考えるとわかりやすい
    #     # OuterRef('room') / 後でメインの問い合わせで指定されるroomを使ってくださいねという「仮の目印」のようなもの

    #     messages = Message.objects.filter(pk=Subquery(latest_message_qs.values('pk')[:1])).order_by('-created_at')
    #     # filter(pk= ... ) / メッセージのユニークID（pk）が ... と一致するものを探す
    #     # Subquery( ... )  / 別の小さな問い合わせを先に実行し、その結果を使う
    #     # latest_message_qs.values('pk')  / latest_message_qsのデータの中からpkの値だけ取り出す
    #     # OuterRef('room')という目印の影響で、データベースは、存在する全てのroomについて、内部的にサブクエリを順番に実行していく
        
    #     ctx['friends_with_messages'] = zip(friends, messages)

    #     return ctx
    #     # 2つ目のモデルを指定できた
    

@login_required
def talk_room(request, pk):
    other_user = get_object_or_404(CustomUser, id=pk)
    me = request.user
    # get_object_or_404はモデルクラスやフィルタ条件を入力すると、モデルからオブジェクトを取得する

    room = Room.get_or_create_room(me, other_user)

    # ルームに結びついたメッセージを逆参照で取得
    messages = room.messages.order_by('created_at')

    if request.method == 'POST':
        text = request.POST.get('text')
        # request.POST は POST リクエストで送信されたデータが入っている辞書のようなオブジェクト
        # .get('キー') で値を取得できる
        if text:
            Message.objects.create(room=room, sender=me, content=text)
            return redirect('talk_room', pk=other_user.pk)

    return render(request, 'myapp/talk_room.html', {
        'room': room,
        'messages': messages,
        'other_user': other_user
    })

def setting(request):
    return render(request, "myapp/setting.html")
