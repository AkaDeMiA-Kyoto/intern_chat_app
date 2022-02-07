from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('friends', views.FriendsView.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.TalkRoomView.as_view(), name='talk_room'),
    #setting
    path('setting', views.SettingView.as_view(), name='setting'),
    path('setting/change_username', views.UsernameChangeView.as_view(), name='change_username'),
    path('setting/change_mail', views.UsermailChangeView.as_view(), name='change_mail'),
    path('setting/change_icon', views.UsericonChangeView.as_view(), name='change_icon'),
    path('setting/complete', views.CompleteView.as_view(), name='complete'),
]