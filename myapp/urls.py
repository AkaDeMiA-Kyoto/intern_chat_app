from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login.as_view(), name='login'),
    path('friends', views.friends, name='friends'),
    path('logout', views.logout.as_view(), name='logout'),
    path('talk_room/<partner>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('setting/password', views.password_change.as_view(), name='password_change'),
    path('setting/<item>', views.change, name='change'), 
    # 上から順に確認しているので、↑とその一つ上のものを交換するとエラーになる。
    # それが嫌だったらchange.htmlとかのactionをちゃんと設定しましょう。
    path('setting/<item>/done', views.change_done, name='change_done'),
]
