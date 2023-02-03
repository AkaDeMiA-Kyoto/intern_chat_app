from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.hashers import make_password
from .models import CustomUser, TalkRoomModel, MessageModel
from . import forms
from .forms import SingupForm, LoginForm, MessageForm

def index(request):
    return render(request, "myapp/index.html")

# def test(request):
#     print('testviewが呼ばれた')
#     test_str = 'test'
#     initial_form_values = {'test_content':test_str}
#     form = TestForm(request.POST or initial_form_values)
#     print('次がform')
#     print(form)
#     return render(request, "myapp/test.html", {'form':form})

# def test_register(request):
#     print(request.POST['test_content'])
#     return redirect('myapp:index')

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
# https://kamatimaru.hatenablog.com/entry/2020/05/12/060236

# https://marsquai.com/745ca65e-e38b-4a8e-8d59-55421be50f7e/05f253f8-c11b-4c91-8091-989eb2600a7b/de4d464b-1e55-47f4-b993-85dad837dcab/

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

class Friends(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/friends.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        friends = CustomUser.objects.exclude(id=1).exclude(id=user.id)
        context["friends"] = friends
        return context

    # 参考

    # https://office54.net/python/django/orm-database-operate

def talk_room(request, user_id, friend_id):
    if request.method == 'GET':
        print('Get Talk Room')
        user = get_object_or_404(CustomUser, pk=user_id) # 自分を取得
        friend = get_object_or_404(CustomUser, pk=friend_id) # 相手を取得
        talk_room = None

        # userとfriendをidが小さい順のリストにする
        talkers = [user, friend]
        talkers.sort(key=lambda user: user.id) 

        # 二人のトークルームがまだ作られているか判断する
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

        # context準備
        user1 = talkers[0]
        user2 = talkers[1]
        initial_form_values = {
            'talk_room_id':talk_room.pk,
            'user_name':user.username,
            'friend_name':friend.username
            }
        form = MessageForm(request.POST or initial_form_values)
        print(form)
        context = {'user': user, 'friend' : friend, 'talk_room' : talk_room, 'user1':user1, 'user2':user2, 'form':form}
        return render(request, "myapp/talk_room.html", context)

            # 参考
            # https://note.nkmk.me/python-dict-list-sort/
            # https://udemy.benesse.co.jp/development/python-work/python-for.html
            # https://qiita.com/aqmr-kino/items/5875c388d5fc405ee606
            # https://opendata-web.site/blog/entry/8/

def send_message(request):
    if request.method == 'POST':
        # メッセージが送られたときの処理を書く
        # form = MessageForm(request.POST)
        print('message sent')

        # messageModel作成
        # request.POST['email']
        print(request.POST['content'])
        print(type(request.POST['content']))
        print(request.POST['talk_room_id'])
        print(type(request.POST['talk_room_id']))
        talk_room = TalkRoomModel.objects.get(id=int(request.POST['talk_room_id']))
        MessageModel.objects.create(
            talk_room=talk_room, 
            speaker_name = CustomUser.objects.get(username=request.POST['user_name']).username, 
            content=request.POST['content']
            )
        
        # redirect処理(TalkRoomに戻す)
        user_id = CustomUser.objects.get(username=request.POST['user_name']).id
        friend_id = CustomUser.objects.get(username=request.POST['friend_name']).id
        return redirect('myapp:talk_room', user_id=user_id, friend_id=friend_id)


# class Friends(LoginRequiredMixin, ListView):
#     template_name = 'myapp/friends.html'
#     model = CustomUser

# def friends(request, pk):
#     user = CustomUser.objects.get(pk=pk)
#     friends = CustomUser.objects.all()
#     context = {'user':user, 'friends': friends}
#     return render(request, "myapp/friends.html", context)

# class Talk_room(LoginRequiredMixin, TemplateView):
#     template_name = 'myapp/talk_room.html'
    
