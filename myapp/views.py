from django.db.models import Q, Max
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
        user_id = self.request.user.id
        context = super().get_context_data(**kwargs)
        friends_exclude_me = CustomUser.objects.exclude(id=user_id)
        search_word = self.request.GET.get('query')

        if search_word:
            friend_list = friends_exclude_me.filter(username__icontains=search_word)
        else:
            friend_list = friends_exclude_me

        exist_friend_talk = friend_list.raw(
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
                    t.msg_date desc
                ) rownum,
                t.content as content,
                t.msg_date as msg_date
                FROM myapp_customuser u 
                LEFT OUTER JOIN myapp_message t 
                    ON (u.id=t.sender_id OR u.id=t.receiver_id)
                WHERE (t.sender_id={user_id} OR t.receiver_id={user_id}) AND NOT u.id={user_id}
            ) f
            WHERE f.rownum=1
            ORDER BY f.msg_date DESC;
            """)

        not_exist_friend_talk = friend_list.annotate(
            sender__msg_date__max=Max("sender__msg_date", filter=Q(sender__receiver=user_id)),
            receiver__msg_date__max=Max("receiver__msg_date", filter=Q(receiver__sender=user_id)),
        ).filter(sender__msg_date__max=None, receiver__msg_date__max=None).order_by("id")

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
        context['username'] = friend.username
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