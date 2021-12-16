from django.urls import path
from . import views


app_name = 'myapp'

urlpatterns = [
   path('',views.IndexView.as_view(),name="index"),
   path('friends',views.FriendsView.as_view(),name='friends'),
   path('settings',views.SettingsView.as_view(),name='settings'),
   path('username_change',views.UserNameChangeView.as_view(),name='username_change'),
   path('username_change_done',views.UserNameChangeDoneView.as_view(),name='username_change_done'),
   path('image_change',views.ImageChangeView.as_view(),name='image_change'),
   path('image_change_done',views.ImageChangeDoneView.as_view(),name='image_change_done'),

   # トーク画面
   # 誰とのトークかを、URLにて判別
   # ユーザーidに重複が許されていないので、ユーザーidで判別
   path("talk_room/<int:user_id>/", views.TalkRoomView.as_view(), name="talk_room"),
]
