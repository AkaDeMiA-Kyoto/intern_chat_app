from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from myapp.models import CustomUser
from django.views import View
from chat.models import Messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from allauth.account.forms import LoginForm
from django.db.models import OuterRef, Subquery, Q, Max
from django.db.models.functions import Coalesce, Greatest


class UpdateMessage(View):
    
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=400)
    
    def get(self, request, *args, **kwargs):
        sender = self.kwargs.get('sender')
        receiver =  self.kwargs.get('receiver')
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        for message in messages:
            message.seen = True
            message.save()
        serializer = MessageSerializer(instance=messages, many=True)
        return JsonResponse(serializer.data, safe=False)


class Home(TemplateView):
    #Home画面を表示するビュー
    template_name = 'myapp/home.html'

class ChatRoom(TemplateView):
    #Home画面を表示するビュー
    template_name = 'chat/chat_box.html'

def getFriendsList(username):
    """
    指定したユーザの友達リストを取得
    :param: ユーザ名
    :return: ユーザ名の友達リスト
    """
    try:
        user = CustomUser.objects.get(username=username)
        friends = list(user.user_friends.all())
        return friends
    except:
        return []
    
class SearchUser(View):
    
    def get(self, request, *args, **kwargs):
        user_list = []
        me = CustomUser.objects.get(username=request.user.username)
        user = CustomUser.objects.all().exclude(username=request.user.username)
        latest_msg = Messages.objects.filter(
        Q(sender_name=OuterRef("pk"), receiver_name=me)|   Q(sender_name=me, receiver_name=OuterRef("pk"))
        ).order_by("-time")
        user_list = user.annotate(
        send_max=Max("sender__timestamp", filter=Q(sender__receiver_name=me)),
        receive_max=Max("receiver__timestamp", filter=Q(receiver__sender_name=me)),
        latest_time=Greatest("send_max", "receive_max"),
        time=Coalesce("latest_time", "send_max", "receive_max"),
        latest_msg_talk=Subquery(latest_msg.values("description")[:1])
        )
        if 'search' in self.request.GET:
            query = request.GET.get("search")
            users = list(CustomUser.objects.all())
            user_list = user_list.filter(
                    Q(username__icontains=query)            
                    | Q(email__icontains=query)            
                    | Q(latest_msg_talk__icontains=query)   
                )

        friends = getFriendsList(request.user.username)  #自分のフレンド一覧を取得
        return render(request, "chat/search.html", {'friends': user_list, 'friend': friends})
    
class Login(TemplateView):
    template_name = 'chat/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()  # フォームインスタンスをコンテキストに追加
        return context

def addFriend(request, username):
    """
    引数で受け取ったユーザ名(username)を Friendsテーブルに友達として登録する。
    """
    login_user = request.user.username
    friend = CustomUser.objects.get(username=username)
    current_user = CustomUser.objects.get(username=login_user)
    friend_lists = current_user.user_friends.all()
    #既に友達登録済みの場合flag=1にセット
    flag = 0
    for friend_list in friend_lists:
        if friend_list.friend.pk == friend.pk:
            flag = 1
            break
    #フレンド未登録の場合
    if flag == 0:
        #お互いにフレンド登録を行う。
        current_user.user_friends.create(friend=friend)  #ログオンユーザ視点でフレンドを登録
        friend.user_friends.create(friend=current_user)   #フレンド視点でログオンユーザをフレンドに登録
    return redirect("chat:search_user")

def get_message(request, username):  
    friend = CustomUser.objects.get(username=username)
    current_user = CustomUser.objects.get(username=request.user.username)
    messages = Messages.objects.filter(sender_name=current_user.id, receiver_name=friend.id
    ).select_related('sender_name', 'receiver_name') | \
            Messages.objects.filter(sender_name=friend.id, receiver_name=current_user.id
    ).select_related('sender_name', 'receiver_name')
    friends = getFriendsList(request.user.username)
    
    return render(request, "chat/messages.html",
                    {'messages': messages,
                    'friends': friends,
                    'current_user': current_user, 'friend': friend})
