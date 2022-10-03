from django.shortcuts import redirect, render
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from . import forms
from .models import MyUser, ChatContent
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


def index(request):
    # すでにログイン済みのユーザーがインデックスに訪れた場合、リダイレクトさせる
    if request.user.is_authenticated:
        return redirect('myapp:friends')
    return render(request, "myapp/index.html")


@login_required
def friends(request):
    friend_list = MyUser.objects.all().order_by('pub_date')
    return render(request, "myapp/friends.html", {'friends': friend_list})


@login_required
def talk_room(request, friend_id):
    if request.method == 'POST':
        form = forms.ChatForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # フォームの情報をコミットせずに保存（追加情報を登録するため）
            post.pub_date = timezone.now()  # 登録日時の設定
            post.send_to = MyUser.objects.get(pk=friend_id)  # 誰に送るか
            post.send_from = request.user  # 誰から送られるか
            post.save()
            return redirect('myapp:talk_room', friend_id)
        else:
            print(form.errors)  # 要修正
    else:
        contents = ChatContent.objects.filter((Q(send_from__id=request.user.id) & Q(send_to__id=friend_id)) | (Q(send_from__id=friend_id) & Q(send_to__id=request.user.id))).order_by('pub_date')
        form = forms.ChatForm()
        context = {
            'contents': contents,
            'id': friend_id,
            'form': form,
            'partner': MyUser.objects.get(pk=friend_id),
        }
        return render(request, "myapp/talk_room.html", context)


@login_required
def setting(request):
    return render(request, "myapp/setting.html")


def name_change(request):
    if request.method == 'POST':
        form = forms.NameChangeForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data["username"]
            user_obj = MyUser.objects.get(pk=request.user.id)
            user_obj.username = new_name
            user_obj.save()
            return redirect('myapp:setting')
        else:
            print('error')
            context = {
                'form': form
            }
    else:
        context = {
            'form': forms.NameChangeForm()
        }
    return render(request, "myapp/name_change.html", context)


def email_add(request):
    if request.method == 'POST':
        form = forms.EmailChangeForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data["email"]
            user_obj = MyUser.objects.get(pk=request.user.id)
            user_obj.email = new_email
            user_obj.save()
            return redirect('myapp:setting')
        else:
            context = {
                'form': form
            }
    else:
        context = {
            'form': forms.EmailChangeForm()
        }
    return render(request, "myapp/email_add.html", context)


def icon_change(request):
    if request.method == 'POST':
        form = forms.IconChangeForm(request.POST, request.FILES)
        if form.is_valid():
            new_img = form.cleaned_data["img"]
            user_obj = MyUser.objects.get(pk=request.user.id)
            user_obj.img = new_img
            user_obj.save()
            return redirect('myapp:setting')
        else:
            print('error')
            context = {
                'form': form
            }
    else:
        context = {
            'form': forms.IconChangeForm()
        }
    return render(request, "myapp/icon_change.html", context)
