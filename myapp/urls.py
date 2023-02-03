from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.Login.as_view(), name='login'),
    # path('friends/<int:pk>', views.friends, name='friends'),
    path('friends', views.Friends.as_view(), name='friends'),
    path('talk_room/<int:user_id>/<int:friend_id>', views.talk_room, name='talk_room'),
    path('send_message', views.send_message, name='send_message'),
    path('setting', views.setting, name='setting'),
    path('register', views.register, name='register'),
    # path('test', views.test, name='test'),
    # path('test_register', views.test_register, name='test_register')
]

