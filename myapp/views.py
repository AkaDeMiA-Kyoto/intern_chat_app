from django.shortcuts import redirect, render
from .forms import (
    CustomSignupForm,
    UsernameChangeForm,
    # EmailChangeForm,
    ImageChangeForm,
)
from django.views import View
from django.views.generic import TemplateView, FormView, DeleteView, UpdateView
from allauth.account.views import SignupView
from .models import CustomUser, Message
from django.db.models import Q, F, OuterRef, Subquery, DateTimeField, CharField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from allauth.account.utils import send_email_confirmation


class IndexView(TemplateView):
    template_name = "myapp/index.html"


class CustomSignupView(SignupView):
    form_class = CustomSignupForm


class FriendsListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "myapp/friends.html"
    context_object_name = "users"

    def get_queryset(self):
        query = self.request.GET.get("searchtext")
        users = CustomUser.objects.exclude(id=self.request.user.id)

        if query:
            users = users.filter(username__icontains=query)

        current_user = self.request.user

        latest_message = Message.objects.filter(
            Q(send_by=current_user, send_to=OuterRef("pk"))
            | Q(send_to=current_user, send_by=OuterRef("pk"))
        ).order_by("-created_at")[:1]

        users = users.annotate(
            latest_message_time=Subquery(
                latest_message.values("created_at"), output_field=DateTimeField()
            ),
            latest_message_content=Subquery(
                latest_message.values("content"), output_field=CharField()
            ),
        )

        users = users.order_by(
            F("latest_message_time").desc(nulls_last=True), "-created_at"
        )

        return users


class TalkRoomView(LoginRequiredMixin, View):
    template_name = "myapp/talk_room.html"

    def get(self, request, user_id):
        current_user_id = request.user.id

        messages = (
            Message.objects.filter(
                (
                    Q(send_by_id=current_user_id, send_to_id=user_id)
                    | Q(send_by_id=user_id, send_to_id=current_user_id)
                )
            )
            .select_related("send_by", "send_to")
            .order_by("created_at")
        )

        context = {
            "received_user": CustomUser.objects.get(id=user_id),
            "messages": messages,
        }
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        received_user = CustomUser.objects.get(id=user_id)
        current_user = request.user
        content = request.POST.get("content")

        if content:
            Message.objects.create(
                content=content,
                send_to=received_user,
                send_by=current_user,
            )

        return redirect("talk_room", user_id=user_id)


class SettingView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"


class ChangeUsernameView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UsernameChangeForm
    template_name = "myapp/change_username.html"
    success_url = reverse_lazy("setting")

    def get_object(self, queryset=None):
        return self.request.user


class ChangeImageView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ImageChangeForm
    template_name = "myapp/change_image.html"
    success_url = reverse_lazy("setting")

    def get_object(self, queryset=None):
        return self.request.user


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy("account_login")

    def get_object(self, queryset=None):
        return self.request.user


def send_custom_email_confirmation(user, request):
    expiration_time = 1

    send_email_confirmation(
        request,
        user,
        context={"expiration_time": expiration_time},
    )
