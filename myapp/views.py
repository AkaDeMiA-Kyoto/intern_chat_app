import re

from django.contrib.auth.views import (
        LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
        )
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
        TemplateView, CreateView, UpdateView
        )
from .forms import (
        SignupForm, LoginForm, TalkRoomForm, UpdateUsernameForm, UpdateMailaddressForm, UpdateIconForm
        )
from .models import User, Talk

class IndexView(TemplateView):
    template_name = "myapp/index.html"

class SignupView(CreateView):
    template_name = "myapp/signup.html"
    form_class = SignupForm

class LoginView(LoginView):
    template_name = "myapp/login.html"
    authentication_form = LoginForm

class LogoutView(LogoutView):
    pass

class FriendsListView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/friends.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_keyword = self.request.GET.get('search_keyword')

        friends = User.objects.all().filter(~Q(username=self.request.user))
        talks = Talk.objects.all().order_by("-sent_time").values()

        friends_dic = []
        for friend in friends:
        #     # 検索キーワードが指定されていてそれが何にも合致していなければ飛ばす
            if (search_keyword == None or 
                    re.search(search_keyword, friend.username) or 
                    re.search(search_keyword, friend.email)):
                    talk_found = False
                    for talk in talks:
                        if ((talk["sender_id"] == self.request.user.id and 
                            talk["receiver_id"] == friend.id) or
                            (talk["sender_id"] == friend.id and 
                                talk["receiver_id"] == self.request.user.id)):
                            friends_dic.append({
                                "id": friend.id,
                                "username": friend.username,
                                "icon": friend.icon,
                                "message": talk["message"],
                                "sent_time": talk["sent_time"],
                                })
                            talk_found = True
                            break
                    if not talk_found:
                        friends_dic.append({
                            "id": friend.id,
                            "username": friend.username,
                            "icon": friend.icon,
                            "message":"",
                            "sent_time": "",
                            })


        context["friends"] = friends_dic
        return context

class TalkRoomView(LoginRequiredMixin, CreateView):
    template_name = "myapp/talk_room.html"
    form_class = TalkRoomForm

    def get_success_url(self):
        return reverse_lazy("talk_room", args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_id = self.kwargs['pk']
        friend_username = User.objects.get(id=friend_id)
        context["friend_id"] = friend_id
        context["friend_username"] = friend_username
        # N+1問題解消
        context["talks"] = Talk.objects.select_related().all().filter(
            Q(sender = self.request.user, receiver=friend_username)
            |   Q(sender=friend_username, receiver=self.request.user)
        ).order_by("sent_time")
        return context

    def form_valid(self, form):
        talk = form.save(commit=False)
        talk.sender = self.request.user
        talk.receiver = User.objects.get(id=self.kwargs['pk'])
        talk.save()
        return super().form_valid(form)


#各種設定
class SettingView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"

class UpdateUsernameView(LoginRequiredMixin, UpdateView):
    template_name ="myapp/setting_username.html"
    model = User
    form_class = UpdateUsernameForm
    success_url = reverse_lazy("username_updated")

    def get_object(self):
        return self.request.user

class UpdateMailaddressView(LoginRequiredMixin, UpdateView):
    template_name ="myapp/setting_mailaddress.html"
    model = User
    form_class = UpdateMailaddressForm
    success_url = reverse_lazy("mailaddress_updated")

    def get_object(self):
        return self.request.user

class UpdateIconView(LoginRequiredMixin, UpdateView):
    template_name ="myapp/setting_icon.html"
    model = User
    form_class = UpdateIconForm
    success_url = reverse_lazy("icon_updated")

    def get_object(self):
        return self.request.user

class UpdatePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "myapp/setting_password.html"
    success_url = reverse_lazy("password_updated")

#設定完了
class UpdateUsernameCompletedView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting_username_completed.html"

class UpdateMailaddressCompletedView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting_mailaddress_completed.html"

class UpdateIconCompletedView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting_icon_completed.html"

class UpdatePasswordCompletedView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "myapp/setting_password_completed.html"
