from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.hashers import make_password
from .models import CustomUser, TalkRoomModel, MessageModel
from . import forms
from .forms import SingupForm, LoginForm, MessageForm, NameChangeForm, EmailChangeForm, IconChangeForm
from django.utils import timezone
from django.urls import reverse_lazy

def base(request):
    return render(request, "myapp/base.html")

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    form = forms.SingupForm()
    return render(request, "myapp/signup.html", {'form': form})

def login_view(request):
    return render(request, "myapp/login.html")

def setting(request):
    return render(request, "myapp/setting.html")

def register(request):
    if request.method == 'POST':
        form = SingupForm(request.POST,request.FILES)
        if form.is_valid():
            print('ok')
            # ユーザー登録
            CustomUser.objects.create(
                username=request.POST['username'], 
                email=request.POST['email'], 
                password=make_password(request.POST['password']), 
                icon_image=request.FILES['image']
                )
            return redirect('myapp:index')
        else:
            print('is not ok')
            answer = form
            form = SingupForm()
            context = {
                'form' : form,
                'answer' : answer
            }
            return render(request, "myapp/signup.html", context)

# 参考
# DjangoでUserモデルのインスタンスにpasswordをsetするときにはset_passwordメソッドを使う https://kamatimaru.hatenablog.com/entry/2020/05/12/060236

# Django2:独自のパスワード認証を作る際に便利なメソッド紹介 https://marsquai.com/745ca65e-e38b-4a8e-8d59-55421be50f7e/05f253f8-c11b-4c91-8091-989eb2600a7b/de4d464b-1e55-47f4-b993-85dad837dcab/

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

class Friends(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/friends.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # friendの並び替え
        message_friends = [] # message送信をしたことがあるfriendのリスト ({Model, latest_message_date}の辞書リスト)
        non_message_friends = [] # message送信をしたことがないfriendのリスト ({Model, id}の辞書リスト)

        # まずは順番を気にせず、それぞれのリストを作る
        for friend in CustomUser.objects.exclude(id=1).exclude(id=user.id):
            # まずは、メッセージを送ったことがあるか確認していく
            # 部屋が作られているかどうかを確認
            is_room_exist = False
            for room in TalkRoomModel.objects.all():
                for person in room.users.all():
                    if person in [user, friend]:
                        is_room_exist = True
                    else:
                        is_room_exist = False
                        break
                if is_room_exist: # トークルームがあれば
                    if room.latest_message_date is not None: # メッセージを送ったことがあれば、最後のメッセージ内容と時間を辞書にして、messag_friendsに追加
                        message_friends.append({'friend':friend, 'latest_message_date':room.latest_message_date, 'latest_message_content':room.latest_message_content})
                    else:
                        non_message_friends.append({'friend':friend, 'id':friend.id})
                    break
            if not is_room_exist: # トークルームがなければ、
                non_message_friends.append({'friend':friend, 'id':friend.id})
        # リストの順番を整える
        message_friends.sort(key=lambda x: x['latest_message_date'])
        message_friends.reverse()
        non_message_friends.sort(key=lambda x: x['id'])

        # friendsリストを作る
        friends_dicts = []
        for friend_dict in message_friends:
            friends_dicts.append({
                'friend':friend_dict['friend'],
                'is_sent_message':True,
                'latest_message_date':friend_dict['latest_message_date'],
                'latest_message_content':friend_dict['latest_message_content']
                })
        for friend_dict in non_message_friends:
            friends_dicts.append({
                'friend':friend_dict['friend'],
                'is_sent_message':False
            })
        
        context["user"] = user
        context["friends_dicts"] = friends_dicts
        return context

    # 参考
    # 【Django】データベース操作（取得・作成・更新・削除）：ORMの利用 https://office54.net/python/django/orm-database-operate

def talk_room(request, user_id, friend_id):
    if request.method == 'GET':
        print('Get Talk Room')
        user = get_object_or_404(CustomUser, pk=user_id) # 自分を取得
        friend = get_object_or_404(CustomUser, pk=friend_id) # 相手を取得
        talk_room = None

        # userとfriendをidが小さい順のリストにする
        talkers = [user, friend]
        talkers.sort(key=lambda user: user.id) 

        # 二人のトークルームがまだ作られていないか判断する
        is_room_exist = False
        for room in TalkRoomModel.objects.all():
            for person in room.users.all():
                if person in talkers:
                    is_room_exist = True
                else:
                    is_room_exist = False
                    break
            if is_room_exist: # トークルームがあれば、移動先として指定
                talk_room = room # 移動先のトークルーム指定
                print('talk_room already exist')
                break

        # トークルームがなければ、作って移動先に指定
        if not is_room_exist: 
            # 新しくtalkRoomを作る
            new_talk_room = TalkRoomModel.objects.create()
            for talker in talkers:
                new_talk_room.users.add(talker)
            new_talk_room.save()
            print('created new talk_room')
            talk_room = new_talk_room # 移動先のトークルーム指定

        # print(talk_room.users.order_by()[0])

        # messageリスト準備
        users_messages = talk_room.messagemodel_set.all().order_by('date') # talk_roomに入っているmessageを取得,並び替え

        # 参考
        # Djangoのorder_byについていろいろな使い方をまとめました https://www.nblog09.com/w/2019/02/03/django-order-by/

        # context準備
        user1 = talkers[0]
        user2 = talkers[1]
        initial_form_values = {
            'talk_room_id':talk_room.pk,
            # 'user_name':user.username,
            'user_id':user.id,
            'friend_id':friend.id
            }
        form = MessageForm(request.POST or initial_form_values)
        context = {'user': user, 'friend' : friend, 'talk_room' : talk_room, 'user1':user1, 'user2':user2, 'form':form, 'messages':users_messages}
        return render(request, "myapp/talk_room.html", context)

            # 参考
            # Pythonで辞書のリストを特定のキーの値に従ってソート https://note.nkmk.me/python-dict-list-sort/
            # python for文を初心者向けに解説！for文基礎はこれで完璧 https://udemy.benesse.co.jp/development/python-work/python-for.html
            # Djangoの多対多関係モデルで簡易タグ機能を作る https://qiita.com/aqmr-kino/items/5875c388d5fc405ee606
            # https://opendata-web.site/blog/entry/8/

def send_message(request):
    if request.method == 'POST':
        # メッセージが送られたときの処理を書く
        # form = MessageForm(request.POST)
        print('message sent')

        # messageModel作成
        # request.POST['email']
        talk_room = TalkRoomModel.objects.get(id=int(request.POST['talk_room_id']))
        MessageModel.objects.create(
            talk_room=talk_room, 
            # speaker_name = CustomUser.objects.get(username=request.POST['user_name']).username, 
            speaker_id = CustomUser.objects.get(id=request.POST['user_id']).id,
            content=request.POST['content']
            )
        # talk_roomに最新メッセージの時刻と内容を記録
        talk_room.latest_message_date = timezone.now()
        talk_room.latest_message_content = request.POST['content']
        talk_room.save()
        
        # redirect処理(TalkRoomに戻す)
        user_id = CustomUser.objects.get(id=int(request.POST['user_id'])).id
        friend_id = CustomUser.objects.get(id=int(request.POST['friend_id'])).id
        return redirect('myapp:talk_room', user_id=user_id, friend_id=friend_id)

class Logout(LoginRequiredMixin, LogoutView):
    template_name = "myapp/logout.html"

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('myapp:password_change_done')
    template_name = 'myapp/password_change.html'

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更完了"""
    template_name = 'myapp/password_change_done.html'

# 参考
# Python + Djangoでパスワード変更画面を実装する https://qiita.com/t-iguchi/items/67430e164de0e6701dc8

class NameChange(LoginRequiredMixin, TemplateView):
    def get(self,request):
        changed_inf = 'name'
        initial_values = {'old_password_data':self.request.user.password, 'changed_inf':changed_inf}
        form = NameChangeForm(request.POST or initial_values)
        change_inf = '名前' # 変更する情報が何か（ページに表示する用)
        context = {'form':form, 'change_inf':change_inf}
        return render(request, "myapp/account_inf_change.html", context)

class EmailChange(LoginRequiredMixin, TemplateView):
    def get(self,request):
        changed_inf = 'email'
        initial_values = {'old_password_data':self.request.user.password, 'changed_inf':changed_inf}
        form = EmailChangeForm(request.POST or initial_values)
        change_inf = 'メールアドレス' # 変更する情報が何か（ページに表示する用)
        context = {'form':form, 'change_inf':change_inf}
        return render(request, "myapp/account_inf_change.html", context)

class IconChange(LoginRequiredMixin, View):
    def get(self,request):
        changed_inf = 'icon'
        initial_values = {'old_password_data':self.request.user.password, 'changed_inf':changed_inf}
        form = IconChangeForm(request.POST or initial_values)
        change_inf = 'アイコン' # 変更する情報が何か（ページに表示する用)
        context = {'form':form, 'change_inf':change_inf}
        return render(request, "myapp/account_inf_change.html", context)

class InfChangeDone(LoginRequiredMixin, View):
    def post(self,request):
        changed_inf = request.POST['changed_inf']
        form = None
        context = None
        print(changed_inf)

        # どのフォームか確認
        if changed_inf == 'name':
            print('name')
            context = {'change_inf':'名前'}
            form = NameChangeForm(request.POST,request.FILES)
        elif changed_inf == 'email':
            print('email')
            context = {'change_inf':'メールアドレス'}
            form =EmailChangeForm(request.POST,request.FILES)
        elif changed_inf == 'icon':
            print('icon')
            context = {'change_inf':'アイコン'}
            form = IconChangeForm(request.POST,request.FILES)

        # 入力が有効であれば（パスワードがあっていれば）
        if form.is_valid():
            user = self.request.user
            if changed_inf == 'name':
                user.username = request.POST['new_username']
                user.save()
            elif changed_inf == 'email':
                user.email = request.POST['new_email']
                user.save()
            elif changed_inf == 'icon':
                user.icon_image=request.FILES['new_image']
                user.save()
            return render(request, 'myapp/inf_change_done.html', context)
        else: # 入力が無効であれば（パスワードが間違っていれば）
            print('is not ok')
            answer = form
            initial_values = {'old_password_data':self.request.user.password, 'changed_inf':changed_inf}
            change_inf = None
            if changed_inf == 'name':
                form = NameChangeForm(request.POST or initial_values)
            elif changed_inf == 'email':
                form =EmailChangeForm(request.POST or initial_values)
            elif changed_inf == 'icon':
                form = IconChangeForm(request.POST or initial_values)
            context['form'] = form
            context['answer'] = answer
            return render(request, "myapp/account_inf_change.html", context)

# 参考
# 【Django】ログアウト機能の実装方法【LogoutView】 https://kosuke-space.com/django-logoutview
# 【Django】クラスベースビュー(Class-based View)の操作入門｜PythonでWebアプリ開発#12 https://di-acc2.com/programming/python/5210/

# 参考
# Djangoのタイムゾーンを日本に変更。setting.pyのTIME_ZONEをAsia/Tokyoに。 https://katana-neko.com/20200909/django-timezone/
    
