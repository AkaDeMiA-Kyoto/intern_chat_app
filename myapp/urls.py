from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import friends




urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignUpView.as_view(), name='signup_view'),
    path('login', views.loginview.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('finish',views.finish, name='finish'),
    path('logout/', views.logoutview.as_view(), name='logout'),

     # ユーザー名変更ページ
    path('username', views.change_username, name='change_username'),

    # メールアドレス変更ページ
    path('email', views.change_email, name='change_email'),

    # アイコン変更ページ
    path('icon', views.change_icon, name='change_icon'),

    # パスワード変更ページ
    path('password', views.MyPasswordChangeView.as_view(), name='change_password'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

LOGIN_REDIRECT_URL = 'friends'  # ログイン成功時のリダイレクト先
