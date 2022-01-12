from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, LogoutView
from django.db.models import Q, Max
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import templatize
from django.views import generic

from .models import CustomUser, Message
from .forms import CustomSignUpForm, MessageForm, ChangeUsernameForm, ChangeEmailForm, ChangeImageForm


class IndexView(generic.TemplateView):
    template_name = "index.html"


class SignUpView(generic.TemplateView):
    template_name = "myapp/signup.html"
    form_class = CustomSignUpForm

    def get(self, request):
        form = CustomSignUpForm()
        return render(request, {'form': form})

    def post(self, request):
        form = CustomSignUpForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, {'form':form})


class FriendsView(LoginRequiredMixin, generic.ListView):
    template_name = "myapp/friends.html"

    def get_queryset(self):
        user = self.request.user
        # 土佐さんありがとうございました！
        friends = CustomUser.objects.raw(
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
                    t.sendtime desc
                ) rownum,
                t.sendtime as sendtime,
                t.content as content
                FROM myapp_customuser u 
                LEFT OUTER JOIN myapp_message t 
                    ON (u.id=t.sender_id OR u.id=t.receiver_id)
                WHERE (t.sender_id={user.id} OR t.receiver_id={user.id}) AND NOT u.id={user.id}
            ) f
            WHERE f.rownum=1;
            """)
        # こっちも土佐さんありがとうございました！
        unknown_friends = CustomUser.objects.exclude(id=user.id).annotate(
            sender__sendtime__max=Max("sender__sendtime", filter=Q(sender__receiver=user)),
            receiver__sendtime__max=Max("receiver__sendtime", filter=Q(receiver__sender=user)),
        ).filter(sender__sendtime__max=None, receiver__sendtime__max=None).order_by("id")

        return friends, unknown_friends

    def get_context_data(self):
        context = super().get_context_data()
        friends, unknown_friends = self.get_queryset()
        context["user"] = self.request.user.username
        context["header_title"] = "友だち"
        context["friends"] = friends
        context["unknown_friends"] = unknown_friends
        return context


class TalkRoomView(LoginRequiredMixin, generic.ListView):
    template_name = "myapp/talk_room.html"

    def get_queryset(self, **kwargs):
        me = self.request.user
        you = CustomUser.objects.get(id=self.kwargs["your_id"])
        queryset = Message.objects.select_related('sender', 'receiver').filter( Q(sender=me) | Q(receiver=me) ).filter( Q(sender=you) | Q(receiver=you) ).order_by("sendtime")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        me = self.request.user
        you = CustomUser.objects.get(id=self.kwargs["your_id"])
        data = self.get_queryset()
        context['sender'] = me
        context["receiver"] = you
        context["data"] = data
        context["form"] = MessageForm()
        return context

    def post(self, request, **kwargs):
        form = MessageForm(request.POST)
        you = CustomUser.objects.get(id=self.kwargs["your_id"])
        if form.is_valid():
            newrecord = Message(
                sender = self.request.user,
                receiver = you,
                content = form.cleaned_data["content"],
            )
            newrecord.save()
            return self.get(request, **kwargs)


class SettingView(LoginRequiredMixin, generic.TemplateView):
    template_name = "myapp/setting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["user"] = self.request.user
        context["header_title"] = "設定"
        return context


class ChangeUsernameView(LoginRequiredMixin, generic.TemplateView):
    template_name = "myapp/change_username.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["change_url"] = "myapp:change_username"
        context["header_title"] = "ユーザ名変更"
        context["label"] = "新しいユーザ名："
        context["form"] = ChangeUsernameForm()
        return context

    def post(self, request, **kwargs):
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data["username"]
            request.user.save()
            return redirect(to="/change_setting_done/change_username")
        return redirect(to="myapp:change_username")


class ChangeEmailView(LoginRequiredMixin, generic.TemplateView):
    template_name = "myapp/change_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["change_url"] = "myapp:change_email"
        context["form_label"] = "email"
        context["header_title"] = "Eメール変更"
        context["label"] = "新しいEメールアドレス："
        context["form"] = ChangeEmailForm()
        return context

    def post(self, request, **kwargs):
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            return redirect(to="/change_setting_done/change_email")
        return redirect(to="myapp:change_email")
    
class ChangeImageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "myapp/change_image.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["change_url"] = "myapp:change_image"
        context["header_title"] = "アイコン変更"
        context["label"] = "新しいアイコン"
        context["form"] = ChangeImageForm()
        return context

    def post(self, request, **kwargs):
        form = ChangeImageForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.image = form.cleaned_data["image"]
            request.user.save()
            return redirect(to="/change_setting_done/change_image")
        return redirect(to="myapp:change_image")


class ChangeSettingDoneView(LoginRequiredMixin, generic.TemplateView):
    template_name = "myapp/change_setting_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        chagnge_command = self.kwargs["change_command"]
        if chagnge_command == "change_username":
            context["change_command"] = "ユーザ名の変更"
        elif chagnge_command == "change_email":
            context["change_command"] = "Eメールアドレスの変更"
        elif chagnge_command == "change_image":
            context["change_command"] = "アイコンの変更"
        return context


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    '''パスワード変更ビュー'''
    success_url = reverse_lazy('password_change_done')
    template_name = 'myapp/change_password.html'


class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    '''パスワード変更完了'''
    template_name = 'myapp/change_password_done.html'


class Logout(LogoutView):
    success_url = reverse_lazy("index")