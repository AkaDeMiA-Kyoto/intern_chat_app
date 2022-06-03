from django.contrib.auth.views import (
        LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
        )
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
        TemplateView, CreateView, ListView, UpdateView
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

class FriendsListView(TemplateView, LoginRequiredMixin):
    template_name = "myapp/friends.html"
    def get_context_data(self):
        context = super().get_context_data()
        friends_list = []
        friends_dic = User.objects.all().filter(~Q(username=self.request.user)).values()
        def return_recent_Talk_obj(friend):
            talk_dic = Talk.objects.all().filter(
            Q(sender = self.request.user, receiver=friend)
            |   Q(sender=friend, receiver=self.request.user)
            ).values()
            return talk_dic[len(talk_dic)-1]

        for i in range(len(friends_dic)):
            friends_list.append({
                "id": friends_dic[i]["id"],
                "username": friends_dic[i]["username"],
                "icon": friends_dic[i]["icon"],
                "brief_message": return_recent_Talk_obj(friends_dic[i]["id"])["message"],
                "last_sent": return_recent_Talk_obj(friends_dic[i]["id"])["sent_time"],
                })

        print(friends_list)
        context["friends"] = friends_list

        return context

class TalkRoomView(CreateView, LoginRequiredMixin):
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
        context["talks"] = Talk.objects.all().filter(
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
class SettingView(TemplateView, LoginRequiredMixin):
    template_name = "myapp/setting.html"

class UpdateUsernameView(UpdateView, LoginRequiredMixin):
    template_name ="myapp/setting_username.html"
    model = User
    form_class = UpdateUsernameForm
    success_url = reverse_lazy("username_updated")

    def get_object(self):
        return self.request.user

class UpdateMailaddressView(UpdateView, LoginRequiredMixin):
    template_name ="myapp/setting_mailaddress.html"
    model = User
    form_class = UpdateMailaddressForm
    success_url = reverse_lazy("mailaddress_updated")

    def get_object(self):
        return self.request.user

class UpdateIconView(UpdateView, LoginRequiredMixin):
    template_name ="myapp/setting_icon.html"
    model = User
    form_class = UpdateIconForm
    success_url = reverse_lazy("icon_updated")

    def get_object(self):
        return self.request.user

class UpdatePasswordView(PasswordChangeView, LoginRequiredMixin):
    template_name = "myapp/setting_password.html"
    success_url = reverse_lazy("password_updated")

#設定完了
class UpdateUsernameCompletedView(TemplateView, LoginRequiredMixin):
    template_name = "myapp/setting_username_completed.html"

class UpdateMailaddressCompletedView(TemplateView, LoginRequiredMixin):
    template_name = "myapp/setting_mailaddress_completed.html"

class UpdateIconCompletedView(TemplateView, LoginRequiredMixin):
    template_name = "myapp/setting_icon_completed.html"

class UpdatePasswordCompletedView(PasswordChangeDoneView, LoginRequiredMixin):
    template_name = "myapp/setting_password_completed.html"
