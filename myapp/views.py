from django.contrib.auth import get_user_model
from django .views.generic import View
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserNameChangeForm,ImageChangeForm,TalkForm
from django.db.models import OuterRef, Q, Subquery

from .models import Talk

User = get_user_model()


# 最初の画面
class IndexView(generic.TemplateView):
    template_name = "index.html"
    

# 友達一覧の画面
class FriendsView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "friends.html"
    paginate_by = 7

    def get_queryset(self):
        user = self.request.user

        # 最新のトークも表示する
        # ユーザーひとりずつの最新のトークを特定する
        latest_msg = Talk.objects.filter(
            Q(talk_from=OuterRef("pk"), talk_to=user)
            | Q(talk_from=user, talk_to=OuterRef("pk"))
        ).order_by("-time")

        friends = (
            User.objects.exclude(id=user.id)
            .annotate(
                latest_msg_pk=Subquery(latest_msg.values("pk")[:1]),
                latest_msg_talk=Subquery(latest_msg.values("talk")[:1]),
                latest_msg_time=Subquery(latest_msg.values("time")[:1]),
            )
            .order_by("latest_msg_pk")
        )

        q_word = self.request.GET.get('query')

        if q_word:
            friends = friends.filter(Q(username__icontains=q_word))
        

        return friends



class TalkRoomView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = request.user
        friend = get_object_or_404(User, id=user_id)

        talk = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
        ).order_by("time")

        form = TalkForm()

        context = {
            "form": form,
            "talks": talk,
            "friend": friend,
            "user":user,
        }
        return render(request, "talk_room.html", context)


    def post(self,request, user_id):
        user = request.user
        friend = get_object_or_404(User, id=user_id)

        talk = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
        ).order_by("time")

        form = TalkForm()

        context = {
            "form": form,
            "talks": talk,
            "friend": friend,
            "user":user,
        }

        new_talk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=new_talk)

        # 送信内容があった場合
        if form.is_valid():
            # 保存
            form.save()
            # 更新
            return redirect("myapp:talk_room", user_id)

        return render(request, "talk_room.html", context)








# 設定一覧の画面
class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "settings.html"


class UserNameChangeView(LoginRequiredMixin, View):
    def get(self, request):
	    context = {}
	    form = UserNameChangeForm()
	    context["form"] = form
	    return render(request, 'username_change.html', context)

	    
    def post(self, request):
        form = UserNameChangeForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            user_obj = User.objects.get(username=request.user.username)
            user_obj.username = username
            user_obj.save()
            return redirect("myapp:username_change_done")

class UserNameChangeDoneView(LoginRequiredMixin, generic.TemplateView):
    template_name = "username_change_done.html"



class ImageChangeView(LoginRequiredMixin, View):
    def get(self, request):
	    context = {}
	    form = ImageChangeForm()
	    context["form"] = form
	    return render(request, 'image_change.html', context)

	    
    def post(self, request):
        form = ImageChangeForm(request.POST, request.FILES)
        
        if form.is_valid():
            icon = form.cleaned_data['icon']
            user_obj = User.objects.get(username=request.user.username)
            user_obj.icon = icon
            user_obj.save()
            return redirect("myapp:image_change_done")

class ImageChangeDoneView(LoginRequiredMixin, generic.TemplateView):
    template_name = "image_change_done.html"


