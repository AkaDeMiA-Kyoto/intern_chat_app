from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('base', views.base, name='base'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('friends', views.Friends.as_view(), name='friends'),
    path('talk_room/<int:user_id>/<int:friend_id>', views.talk_room, name='talk_room'),
    path('send_message', views.send_message, name='send_message'),
    path('setting', views.setting, name='setting'),
    path('register', views.register, name='register'),
]

