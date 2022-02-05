from django.shortcuts import redirect, render
from django.db.models import Q
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import(
    CustomUser,
    Message,
)
from .forms import(
    MessageForm,
    UsernameChangeForm,
    UsermailChangeForm,
    UsericonChangeForm,
)

class IndexView(generic.TemplateView):
     template_name = 'myapp/index.html'


def friends(request):
    data = CustomUser.objects.exclude(id=request.user.id)
    # requestuserとトーク履歴のあるユーザー
    list_w_talks = []
    # request.userとトーク履歴のないユーザー
    list_wo_talks = []
    for friend in data:
        latests = Message.objects.all().filter(Q(sender=request.user.id) | Q(receiver=request.user.id))\
            .filter(Q(sender=friend.id) | Q(receiver=friend.id)).order_by("-msg_date").first()
        if latests != None:
            list_w_talks.append([latests.msg_date, friend, latests])
        else:
            list_wo_talks.append([friend.created_date, friend])

    list_w_talks.sort(key=lambda x: x[0] ,reverse=True)
    list_wo_talks.sort(key=lambda x: x[0] ,reverse=True)
    params={
        'data': data,
        'list_w_talks':list_w_talks,
        'list_wo_talks':list_wo_talks,
    }
    return render(request, "myapp/friends.html", params)

class FriendsView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = 'myapp/friends.html'
    #form_class = FriendSearchForm
    #検索機能をつける時に必要なフォームの作成。その際にListViewから違うクラスに帰る必要ありそう。

    #テンプレートに使う辞書データを作成.。メッセージが存在する、しないー＞メッセージの時間順に並べる

    def get_context_data(self, **kwargs):
        
        return super().get_context_data(**kwargs)

    #クエリーセットゲットしたけど、どう使うん？
    def get_queryset(self, request):
        friend = CustomUser.objects.exclude(id=request.user).order_by
        return friend


# def talk_room(request, num):
    # friend = CustomUser.objects.get(id=num)
    # msg_data = Message.objects.filter(Q(sender = request.user) | Q(receiver = request.user))\
    #     .filter(Q(sender = friend) | Q(receiver = friend)).order_by("msg_date")
    # params = {
    #     'username': CustomUser.objects.get(id=num),
    #     'form': MessageForm(),
    #     'data': msg_data,
    # }
    # if (request.method == 'POST'):
    #     obj = Message(receiver=friend, sender=request.user)
    #     form = MessageForm(request.POST, instance=obj)
    #     form.save()
    # return render(request, "myapp/talk_room.html", params)

class TalkRoomView(LoginRequiredMixin, generic.CreateView):
    model = Message
    template_name = 'myapp/talk_room.html'
    form_class = MessageForm
    # pk_url_kwargs = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend = CustomUser.objects.get(id=self.kwargs['pk'])
        msg_data = Message.objects.filter(Q(sender = self.request.user) | Q(receiver = self.request.user))\
        .filter(Q(sender = friend) | Q(receiver = friend)).order_by("msg_date")
        context['username'] = CustomUser.objects.get(id=self.kwargs['pk'])
        context['data'] = msg_data
        return context

    def get_success_url(self):
        return reverse('talk_room', kwargs={'pk':self.kwargs['pk']})
    
    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender = self.request.user
        message.receiver = CustomUser.objects.get(id=self.kwargs['pk'])
        message.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "送信に失敗")
        return super().form_invalid(form)


class SettingView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'myapp/setting.html'


class UsernameChangeView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    template_name = 'myapp/change_username.html'
    form_class = UsernameChangeForm
    success_url = reverse_lazy('complete')

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"失敗しました")
        return super().form_invalid(form)


class UsermailChangeView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    template_name = 'myapp/change_mail.html'
    form_class = UsermailChangeForm
    success_url = reverse_lazy('complete')

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"失敗しました")
        return super().form_invalid(form)    


class UsericonChangeView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    template_name = 'myapp/change_icon.html'
    form_class = UsericonChangeForm
    success_url = reverse_lazy('complete')

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,"失敗しました")
        return super().form_invalid(form)   


class CompleteView(generic.TemplateView):
    template_name = 'myapp/complete.html'