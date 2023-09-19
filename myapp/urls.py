from django.urls import path
from . import views
from .views import Login
from django.contrib.auth.views import LogoutView
# path の第一引数はurlのパターンを表す文字列で、ドメイン部分('http://example.com/')を除いたurlのパス部分に対応。
# ただし、'/'で始まる必要がある。
# 第二引数は、このＵＲＬパターンにアクセスされたときに実行されるビュー関数またはクラスを指定。

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login/', Login.as_view(), name='login_view'),  #ログインページへのパス(ログイン作成時)
    path('change_username', views.ChangeUsername, name='change_username'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('change_email/', views.change_email, name='change_email'),
    path('change_profile_picture/', views.change_profile_picture, name='change_profile_picture'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_password_done/', views.change_password_done, name='change_password_done'),
    # path('logout/', LogoutView.as_view(template_name='myapp/logout.html'), name='logout'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    ]
# /<int:user_id>/
# loginの部分で第２引数に'Login.as_view()'と書いてあって特殊に見えるが、
# これはクラスベースのビューを関数ベースのビューと同じ形で呼び出せるようにするためのもの