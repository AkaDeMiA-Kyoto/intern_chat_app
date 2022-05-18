from django.urls import path
from . import views
from .views import SignUp

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', SignUp.as_view(), name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]
