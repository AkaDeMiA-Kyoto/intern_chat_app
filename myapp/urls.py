from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.ChatLoginView.as_view(), name='login'), #classの呼び出しにはas_view()メソッド必要。
    path('friends/', views.FriendsView.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.TalkroomView.as_view(), name='talk_room'),
    path('setting/', views.Setting.as_view(), name='setting'),
    path('username_change', views.UsernameChangeView.as_view(), name='username_change'),
    path('email_change', views.EmailChangeView.as_view(), name='email_change'),
    path('image_change', views.ImageChangeView.as_view(), name='image_change'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
