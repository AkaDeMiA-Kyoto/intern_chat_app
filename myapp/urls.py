from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('friends', views.FriendsListView.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.TalkRoomView.as_view(), name='talk_room'),
    path('setting', views.SettingView.as_view(), name='setting'),
    path('update_username', views.UpdateUsernameView.as_view(), name='update_username'),
    path('update_mailaddress', views.UpdateMailaddressView.as_view(), name='update_mailaddress'),
    path('update_icon', views.UpdateIconView.as_view(), name='update_icon'),
    path('update_password', views.UpdatePasswordView.as_view(), name='update_password'),
    path('username_updated', views.UpdateUsernameCompletedView.as_view(), name='username_updated'),
    path('mailaddress_updated', views.UpdateMailaddressCompletedView.as_view(), name='mailaddress_updated'),
    path('icon_updated', views.UpdateIconCompletedView.as_view(), name='icon_updated'),
    path('password_updated', views.UpdatePasswordCompletedView.as_view(), name='password_updated'),
]
