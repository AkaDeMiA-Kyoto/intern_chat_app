from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup', views.SignUpView.as_view(), name='signup_view'),
    path('login', views.CustomLoginView.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
]
