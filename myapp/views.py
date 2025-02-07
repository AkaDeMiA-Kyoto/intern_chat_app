from django.shortcuts import redirect, render, get_object_or_404
from .forms import (
    CustomSignupForm,
    UsernameChangeForm,
    EmailChangeForm,
    ImageChangeForm,
)
from django.views import View
from django.views.generic import TemplateView, FormView
from allauth.account.views import SignupView
from .models import CustomUser, Message
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils.timezone import now
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = "myapp/index.html"


class CustomSignupView(SignupView):
    form_class = CustomSignupForm


class FriendsListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "myapp/friends.html"
    context_object_name = "user_objects"

    def get_queryset(self):
        query = self.request.GET.get("searchtext")
        users = CustomUser.objects.exclude(id=self.request.user.id)

        if query:
            users = users.filter(username__icontains=query)

        current_user = self.request.user
        message_users = []
        for user in users:
            received_message = (
                user.received_messages.filter(send_by=current_user)
                .order_by("-created_at")
                .first()
            )
            sent_message = (
                user.sent_messages.filter(send_to=current_user)
                .order_by("-created_at")
                .first()
            )
            latest_message = None

            if received_message and sent_message:
                latest_message = max(
                    received_message, sent_message, key=lambda msg: msg.created_at
                )
            elif received_message:
                latest_message = received_message
            elif sent_message:
                latest_message = sent_message
            else:
                latest_message = None

            message_users.append({"user": user, "latest_message": latest_message})

        sorted_users = sorted(
            message_users,
            key=lambda entry: (
                0 if entry["latest_message"] else 1,
                (
                    -entry["latest_message"].created_at.timestamp()
                    if entry["latest_message"]
                    else -entry["user"].date_joined.timestamp()
                ),
            ),
            reverse=False,
        )

        return sorted_users


class TalkRoomView(LoginRequiredMixin, View):
    template_name = "myapp/talk_room.html"

    def get(self, request, user_id):
        recieved_user = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user

        messages = Message.objects.filter(
            (Q(send_by=current_user) | Q(send_by=recieved_user))
            & (Q(send_to=recieved_user) | Q(send_to=current_user))
        ).order_by("created_at")

        return render(
            request,
            self.template_name,
            {"recieved_user": recieved_user, "messages": messages},
        )

    def post(self, request, user_id):
        recieved_user = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user
        content = request.POST.get("content")

        if content:
            Message.objects.create(
                content=content,
                created_at=now(),
                send_to=recieved_user,
                send_by=current_user,
            )

        return redirect("talk_room", user_id=recieved_user.id)


class SettingView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ChangeUsernameView(LoginRequiredMixin, FormView):
    template_name = "myapp/change_username.html"
    form_class = UsernameChangeForm
    success_url = reverse_lazy("setting")

    def form_valid(self, form):
        current_user = self.request.user
        current_user.username = form.cleaned_data["username"]
        current_user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = "myapp/change_email.html"
    form_class = EmailChangeForm
    success_url = reverse_lazy("setting")

    def form_valid(self, form):
        current_user = self.request.user
        current_user.email = form.cleaned_data["email"]
        current_user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ChangeImageView(LoginRequiredMixin, FormView):
    template_name = "myapp/change_image.html"
    form_class = ImageChangeForm
    success_url = reverse_lazy("setting")

    def form_valid(self, form):
        current_user = self.request.user
        current_user.image = form.cleaned_data["image"]
        current_user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class DeleteUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        current_user = request.user
        current_user.delete()
        return redirect("index")
