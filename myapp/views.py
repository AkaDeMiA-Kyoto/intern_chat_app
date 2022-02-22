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


class FriendsView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = 'myapp/friends.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friends_exclude_me = CustomUser.objects.exclude(id=self.request.user.id)
        search_word = self.request.GET.get('query')

        if search_word:
            friend_list = friends_exclude_me.filter(username__icontains=search_word)
        else:
            friend_list = friends_exclude_me

        exist_friend_talk = []
        not_exist_friend_talk = []
        for friend in friend_list:
            latest_meg = Message.objects.all().filter(Q(sender=self.request.user.id) | Q(receiver=self.request.user.id))\
                .filter(Q(sender=friend.id) | Q(receiver=friend.id)).order_by("-msg_date").first()
            if latest_meg != None:
                exist_friend_talk.append([latest_meg.msg_date, friend, latest_meg])
            else:
                not_exist_friend_talk.append([friend.created_date, friend])

        exist_friend_talk.sort(key=lambda x: x[0], reverse=True)
        not_exist_friend_talk.sort(key=lambda x: x[0], reverse=True)

        context['history'] = exist_friend_talk
        context['no_history'] = not_exist_friend_talk
        return context


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