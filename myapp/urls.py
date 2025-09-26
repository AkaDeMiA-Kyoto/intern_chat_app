<<<<<<< HEAD
from django.urls import path

=======
from django.urls import path, reverse_lazy
>>>>>>> 568a137c735e2253106d8e0a27f94eeb14bead04
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
<<<<<<< HEAD
    path("", views.index, name="index"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.Login.as_view(), name="login"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path("friends/", views.friends, name="friends"),
    # トーク画面
    # 誰とのトークかを、URLにて判別
    # ユーザー名に重複が許されていないので、ユーザー名で判別
    path("talk_room/<int:user_id>/", views.talk_room, name="talk_room"),
    path("setting/", views.setting, name="setting"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("password_change/", views.PasswordChange.as_view(), name="password_change"),
    path("password_change_done/", views.PasswordChangeDone.as_view(), name="password_change_done"),
    path("user_img_change/", views.user_img_change, name="user_img_change"),
    path("user_img_change_done/", views.user_img_change_done, name="user_img_change_done"),
    path("mail_change/", views.mail_change, name="mail_change"),
    path("mail_change_done/", views.mail_change_done, name="mail_change_done"),
    path("username_change/", views.username_change, name="username_change"),
    path("username_change_done/", views.username_change_done, name="username_change_done"),
=======
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('friends', views.friends.as_view(), name='friends'),
    path('talk_room/<str:username>', views.talk_room.as_view(), name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username', views.username.as_view(), name='username'),
    path('email', views.email.as_view(), name='email'),
    path('icon', views.icon.as_view(), name='icon'),
    path('password', auth_views.PasswordChangeView.as_view(
        template_name='myapp/password.html',
        success_url=reverse_lazy('password_change_done'),
        ), name='password'),
    path('password/done', auth_views.PasswordChangeDoneView.as_view(
        template_name='myapp/password_change_done.html',
    ), name='password_change_done'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
>>>>>>> 568a137c735e2253106d8e0a27f94eeb14bead04
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
