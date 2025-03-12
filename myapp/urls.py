from django.urls import path
from . import views

app_name='myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends_view, name='friends'),
    path('talk_room/<int:id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]
