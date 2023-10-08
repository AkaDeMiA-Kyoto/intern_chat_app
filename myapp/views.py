from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, FormMixin
from django.views.generic import ListView
from .models import *
from .forms import *
from django.db.models import Q, F, OuterRef, Subquery
from django.http import HttpResponseRedirect
from django.urls import reverse


class SignupView(CreateView):
    model = CustomUser
    template_name = 'myapp/signup.html'
    form_class = myUserForm
    success_url = "/"

class FriendView(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'myapp/friends.html'
    model = CustomUser
    context_object_name = 'friends'
    form_class = SearchFriendForm
    success_url = 'friends'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = SearchFriendForm()

        context = context | {"id": self.request.user.id, "username": self.request.user.username, "search_form": search_form}
        return context
    
    def get_queryset(self, **kwargs):
        try:
            search_name = self.request.POST.get('username')
        except:
            search_name = None

        lastmsg = Talk_content.objects.filter(
            Q(user_to=self.request.user, user_from=OuterRef('pk'))|Q(user_to=OuterRef('pk'), user_from=self.request.user)
        ).order_by("-time")

        if search_name:
            user_li = CustomUser.objects.filter(
                Q(username__icontains=search_name)& ~Q(username='admin')
                & ~Q(username=self.request.user.username) & ~Q(username='admin') 
                ).annotate(
                lasttalk = Subquery(lastmsg.values('chat_content')[:1]),
            )
            return user_li
        else:
            user_li = CustomUser.objects.filter(
                ~Q(username=self.request.user.username) & ~Q(username='admin') 
                ).annotate(
                lasttalk = Subquery(lastmsg.values('chat_content')[:1]),
            )
            return user_li
        
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        search_form = SearchFriendForm(request.POST)
        if search_form.is_valid():
            return self.form_valid(search_form)
        else:
            return self.form_invalid(search_form)
        
    def form_valid(self, form, **kwargs):
        # フォームが有効な場合の処理

        # 特定のフィールドのデータを取得
        search_name = form.cleaned_data['username']

        # contextに追加
        context = self.get_context_data(**kwargs, object_list=None,)
        context['search_name'] = search_name

        return self.render_to_response(context)

class TalkroomView(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'myapp/talk_room.html'
    model = Talk_content
    context_object_name = 'messages'
    form_class = ChatInputForm

    def form_valid(self, form, **kwargs):
        id1, id2 = self.kwargs['id1'], self.kwargs['id2']
        url = reverse('talk_room', args=[id1, id2])

        return HttpResponseRedirect(url)
    
    def get_context_data(self, **kwargs):
        id1, id2 = self.kwargs['id1'], self.kwargs['id2']
        user1 = CustomUser.objects.get(id=id1)
        user2 = CustomUser.objects.get(id=id2)

        context = super().get_context_data(**kwargs)
        form = ChatInputForm()

        context = context | {"I": user1, "You": user2, "form": form}
        return context
    
    def get_queryset(self):
        id1, id2 = self.kwargs['id1'], self.kwargs['id2']
        user1 = CustomUser.objects.get(id=id1)
        user2 = CustomUser.objects.get(id=id2)

        search_name = self.request.POST.get('username')
        lastmsg = Talk_content.objects.filter(
            Q(user_to=self.request.user, user_from=OuterRef('pk'))|Q(user_to=OuterRef('pk'), user_from=self.request.user)
        ).order_by("-time")

        messages = Talk_content.objects.filter(
                (Q(user_to=user1, user_from=user2) | Q(user_to=user2, user_from=user1)) & ~Q(chat_content="") 
            ).order_by('time').values('time', 'user_from__username', 'user_to__username', 'chat_content') 
        
        return messages
    
    def post(self, request, *args, **kwargs):
        id1, id2 = self.kwargs['id1'], self.kwargs['id2']
        user1 = CustomUser.objects.get(id=id1)
        user2 = CustomUser.objects.get(id=id2)

        chat_content = request.POST["chat_content"]
        new_message = ChatInputForm({"user_from": user1, "user_to": user2, "chat_content": chat_content})
        if new_message.is_valid():
            new_message.save()
            return self.form_valid(new_message)
        else:
            return self.form_invalid(new_message)

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "myapp/setting.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = context | {"content": "Username", "pk": self.request.user.id}
        return context

class ChangeNameView(LoginRequiredMixin, UpdateView):
    template_name = "myapp/setting_change_obj.html"
    model = CustomUser
    form_class = ChangeUserForm
    success_url = '/change_complete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = context | {"content": "Username", "url_name": "change_name", "pk": self.request.user.id}
        return context

class ChangeEmailView(LoginRequiredMixin, UpdateView):
    template_name = "myapp/setting_change_obj.html"
    model = CustomUser
    form_class = ChangeEmailForm
    success_url = '/change_complete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = context | {"content": "Username", "url_name": "change_email", "pk": self.request.user.id}
        return context

class ChangeIconView(LoginRequiredMixin, UpdateView):
    template_name = "myapp/setting_change_obj.html"
    model = CustomUser
    form_class = ChangeIconForm
    success_url = '/change_complete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = context | {"content": "Username", "url_name": "change_icon", "pk": self.request.user.id}
        return context

class MyPasswordChangeView(PasswordChangeView):
    template_name = "myapp/setting_change_obj.html"
    model = CustomUser
    form_class = ChangePWForm
    success_url = '/change_complete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = context | {"content": "Username", "url_name": "change_pw", "pk": self.request.user.id}
        return context
    

index = TemplateView.as_view(template_name = 'myapp/index.html')
logout_view = LogoutView.as_view(template_name = 'myapp/index.html')
signup_view = SignupView.as_view()
login_view = LoginView.as_view(template_name = 'myapp/login.html')
friends = FriendView.as_view()
talk_room = TalkroomView.as_view()
setting = SettingsView.as_view()    
change_name = ChangeNameView.as_view()
change_email = ChangeEmailView.as_view()
change_icon = ChangeIconView.as_view()
change_pw = MyPasswordChangeView.as_view()