import operator
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
# Qクラスは'&(and)'や'or(|)'の使用を可能にするクラス
from django.db.models import (
    Q, Case, When, F, Max, Subquery, OuterRef, Value
)

from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    TemplateView, ListView
)
from django.urls import reverse_lazy
from django.views.generic.edit import BaseCreateView
# もし同じ名前で違うLoginViewをimportしたいとき、後ろに'as 名前'で競合しなくなる
# ↑自作で作った時など
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
# ログインしたユーザーだけが閲覧できる
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    LogInForm,
    SignUpForm,
    TalkForm,
    ChangeEmailForm,
    ChangeUsernameForm,
    ProfilePictureForm,
)
from django.db import models

from .models import (
    Talk, CustomUser
)
from django.db.models.functions import Coalesce
from django.contrib import messages
from functools import reduce
from operator import and_
 
from django.contrib import messages

# CustomUserにアクセス

User = get_user_model()

# class HomeView(LoginRequiredMixin, TemplateView):
#     template_name='friends.html'
#     login_url='/login'

class Login(LoginView):
    template_name='myapp/login.html'
    redirect_authenticated_user = True
    # form_classはこの後作成するフォームを指定します
    form_class= LogInForm

# 複数のクラスを継承するときは、LoginRequiredMixinから継承しないとバグる
    
def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        #エラー文を含む
        form = SignUpForm()
        # エラーが起こった時に適切なエラーメッセージを表示
        error_message = ""
    elif request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            #データベースに保存
            user = form.save()
            # form.cleaned_dataはフォームのデータをクリーン（バリデーションを通過）
            # された状態で提供し、セキュリティとデータの正確性を確保するのに役立ちます
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            # username と password があってるか確認
            # authenticate が間違ってたらNone が入る
            user = authenticate(username=username, password=password)
            # 合ってたらついでにlogin
            # 第二引数の user は「ログインしたいユーザーを渡す」という意味
            if user is not None:
                login(request, user)
            # ログインして一番最初のページに飛ぶ
            return redirect("/")
        else:
            print(form.errors)
        
# usercreateviewを使用すると楽だからやってみるといいbyかずほ
# "form" という名前にさっき定義した fomr = ~~ を埋め込んで、
# "context" としてsighnup.htmlに送信している
    context = {
        "form": form
    }
    # 辞書型を使えば templateに情報が渡される
    # 今回はsignup.htmlの{{　form　}}に渡している
    # renderの第３引数に渡したい変数など(今回は context)
    return render(request, "myapp/signup.html", context)

    # ビュー関数➔テンプレートに値を渡す手順は３つで、
    # 1, 値を辞書にまとめる
    # 2, render時に第３引数で辞書を渡す
    # 3, テンプレート側で{{}}の形で値を埋め込む


def friends(request):
    # Djangoのビュー関数内で現在ログインしているユーザーを取得するためのコード
    # request オブジェクトの user 属性を通じて、現在のユーザー情報に
    # アクセスしています。user にはログインしているユーザーの情報が含まれる。
    # この情報には、ユーザーの名前、メールアドレス、パスワードなどが含まれる可能性がある。
    user = request.user
    # ログインしているユーザー以外のすべてのユーザーを取得するためのコード。具体的には、
    # 'User':Djangoの組み込み'User'モデルクラス。これは、ユーザーの認証やセッション管理に使用される。
    # 'User.objects':'User'モデルに関連付けられたデフォルトのクエリセットマネージャ。これを使用してデータベース内のユーザーオブジェクトにアクセスできる。
    # ここでは、ログインしているユーザーのIDと一致するユーザーオブジェクトを取得しないようにしている。
    # 'id=user.id'：ログインしているユーザーのIDに合致するユーザーオブジェクトを指す。
    # 'objects'は、Djangoのモデルクラスを操作するためのクエリセットマネージャーを指す。
    # クエリセットマネージャーは、データベースとの対話を行うためのメソッドとクエリを提供する。
    # これにより、データベースからデータを取得、作成、更新、削除するための操作を簡単に行うことができる。

    # CustomUser.objects.exclude(id=user.id):
    # この部分は、CustomUser モデルからユーザーの一覧を取得している。
    # ただし、user.id と一致するユーザーは除外される、つまり、自分自身を含まないユーザーの一覧を取得しようとしている。

    # .annotate(...):
    # .annotate() メソッドは、データベースクエリの結果に注釈を追加するために使用される。
    # この注釈は、latest_message_time という名前で定義されている。

    # models.Max(...):
    # Max 関数は、指定されたカラムの最大値を計算する。
    # ここでは、latest_message_time の最大値を計算し、各ユーザーのレコードに付加する。

    # models.Case(...):
    # Case クラスは、条件に基づいてフィールドを計算するために使用する。
    # この場合、条件に応じて最新のメッセージの時間 (talk__time) を選択する。

    # models.When(...):
    # When クラスは、条件を定義します。ここでは、2つの条件があります：

    # Q(talk_from=user, talk_to=models.OuterRef('id'))：ログインユーザーがメッセージの送信者で、相手が外部参照 (OuterRef) のユーザーである場合
    # Q(talk_from=models.OuterRef('id'), talk_to=user)：相手が外部参照 (OuterRef) のユーザーで、ログインユーザーがメッセージの送信者である場合
    # これらの条件が一致する場合、then パラメーターで指定された models.F('talk__time') を選択します。これにより、最新のメッセージの時間が選択されます。

    # output_field=models.DateTimeField():
    # Case 内で計算される値のデータ型を指定します。ここでは、DateTimeField を指定しています。

    # 最終的に、このクエリは latest_message_time を注釈として持つユーザーのリストを取得し、
    # それを latest_message_time の降順で並べ替え、さらに date_joined の昇順で並べ替えています。
    # つまり、最も最新のメッセージを送信したユーザーが先頭に来るようにソートされたユーザーのリストが得られます。


    # ここでviews側のユーザ検索機能を実装しているが、viewでreturnのように何か処理を施したわけではなく、
    # friendsが何であるかの対象を絞り込んだだけ
    # friendsが何かを絞り込んでおけば、後の処理は以前に書いてある通りに行われる。
    keyword  = request.GET.get('keyword')
    friends = CustomUser.objects.exclude(id=user.id)

    if keyword:
        friends = friends.filter(username__icontains=keyword)
        
    # if keyword := request.GET.get('keyword'):でも同じ動作（セイウチ構文）
    # いらないが、意味的にはこういう場合分け
    # else:
    #     friends = friends
    # search=CustomUser.objects.filter

    info = []
    info_have_message = []
    info_have_no_message = []

    # このuserは'use = request.userを指しており、現在のリクエストを行っているユーザーを指している。
    # このQの中のfriendはfriendsの各要素

    for friend in friends:
        latest_message = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_from=friend, talk_to=user)
        ).order_by('time').last()
        if latest_message:
            info_have_message.append([friend, latest_message, latest_message.time])
        else:
            info_have_no_message.append([friend, None, friend.date_joined])

    info_have_message = sorted(info_have_message, key=operator.itemgetter(2), reverse=True)
    info_have_no_message = sorted(info_have_no_message, key=operator.itemgetter(2), reverse=True)

    info.extend(info_have_message)
    info.extend(info_have_no_message)

    # このリストにはまだ要素が含まれていないため、'info' は空の状態。
    # 後でデータが必要になった際に、このリストに要素を追加することができる。

    # Coalesce は () の中から Null ではない値を返す。すべて Null の場合は Null を返す。

    # 時間順に並び替え
    # operator.itemgetter(2)は３番目の要素(時間情報)を抽出してソートする。

    context = {
        "info": info,
    }

    return render(request, "myapp/friends.html", context)

    # render(<<HttpRequest>>, テンプレート)
    


class CustomListView(ListView):
    template_name='myapp/friends.html'
    queryset=CustomUser.objects.order_by('date_joined')



# user_idにより個々のユーザーに対してデータを扱える
def talk_room(request, user_id):
    # ユーザ・友達をともにオブジェクトで取得
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    # 自分➔友達、友達➔自分のトークをすべて取得
    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).order_by("time")
    # 送信フォーム
    form = TalkForm

    context = {
        "form":form,
        "friend":friend,
        "talk":talk
    }

    if request.method == "POST":
        newtalk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=newtalk)
        
        # ()を書くことによりバリデーションを行う。ない場合は常にtrueが返されてしまう。
        if form.is_valid():
            form.save()
            # 更新
            # このようなリダイレクト処理はPOSTのリクエストを初期化し、リクエストをGETに戻すことにより
            # 万一更新処理を連打されてもPOSTのままにさせない等の用途がある
            return redirect("talk_room", user_id)
        else:
            # エラー時 form.errors には エラー内容が格納されている
            print(form.errors)

    #POSTじゃないorPOSTでも入力がないとき
    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")

# if&elseが重なるとき、階層に注意(間違えた)

def ChangeUsername(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save
            return redirect('setting')
    else:
        form = ChangeUsernameForm(instance=request.user)
    return render(request, "myapp/change_username.html", {"form":form})

# instance 引数は、フォームを特定のモデルインスタンスに関連付け、
# そのインスタンスのデータをフォームに表示するのに便利な方法です。
# この場合、request.user は現在のユーザーを表し、
# そのユーザーのメールアドレス情報をフォームに表示し、編集可能にします。

def change_email(request):
    if request.method == 'POST':
        # この行では、request.POSTを使用してユーザーが送信したデータをフォームにバインドし、
        # request.userをフォームのインスタンスとして設定しています。
        # これにより、フォームが現在のユーザーのメールアドレス情報を表示し、
        # 新しいメールアドレスを受け取ることができます。
        form = ChangeEmailForm(request.POST, instance=request.user)
        # フォームがバリデーションを通過した場合、つまりユーザーが正しい形式でデータを送信した場合、
        # この条件がTrueになります。
        if form.is_valid():
            form.save()
            # メールアドレスの変更が成功した場合、ユーザーを設定ページにリダイレクトします。
            return redirect('setting')
    else:
        # リクエストのHTTPメソッドがPOSTでない場合、通常は初回のページ表示時に実行されます。
        # フォームを表示するために必要な初期化を行います。
        # form = ChangeEmailForm(instance=request.user):
        # 初期表示時に、フォームを生成し、既存のユーザーのメールアドレス情報をフォームにセットします。
        form = ChangeEmailForm(instance=request.user)
    
    return render(request, 'myapp/change_email.html', {'form':form})

def change_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('setting')
    else:
        form = ProfilePictureForm()

    return render(request, 'myapp/change_profile_picture.html', {'form':form})



# reverse_lazy:

# reverse_lazy は Django のビューでよく使用されるユーティリティ関数です。
# この関数は、名前付きURLパターンを基に、そのURLの絶対パスを生成するのに使われます。
# 名前付きURLパターンは urls.py 内で name パラメータで指定されるもので、URLを特定の名前で参照するためのものです。
# reverse_lazy は、必要なタイミングまでURLの解決を遅延させることができ、アプリケーションの初期化中には使われません。
# これにより、循環参照などの問題を回避できます。

def change_password(request):
    return PasswordChangeView.as_view(
        template_name='myapp/password_change.html',
        success_url=reverse_lazy('change_password_done')
    )(request)


def change_password_done(request):
    # messages.success(request, 'パスワードの変更が完了しました')
    return PasswordChangeDoneView.as_view(
        template_name='myapp/password_change_done.html'
    )(request)

