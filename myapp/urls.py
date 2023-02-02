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
    path('setting', views.setting, name='setting'),
    path('register', views.register, name='register'),
]

