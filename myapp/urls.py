from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 基本画面
    path('', views.index, name='index'),
    path('login', views.login.as_view(), name='login'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<slug:username>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('signup', views.signup_view, name='signup_view'),
    path('friends', views.login_view.as_view(), name='login_view'),
    path('', views.logout.as_view(), name='logout'),
    # ユーザ名変更
    path('changename', views.name, name='changename'),
    path('updatename', views.updatename, name='updatename'),
    # メールアドレス変更
    path('changemail', views.mail, name='changemail'),
    path('updatemail', views.updatemail, name='updatemail'),
    # アイコン変更
    path('changeicon', views.icon, name='changeicon'),
    path('updateicon', views.updateicon, name='updateicon'),
    # パスワード変更
    path('changepassword', views.PasswordChange.as_view(), name='changepassword'),
    path('updatepassword', views.PasswordChangeDone.as_view(), name='updatepassword')    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)