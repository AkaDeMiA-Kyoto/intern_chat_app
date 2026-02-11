from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup'),
    path('login', LoginView.as_view(template_name="myapp/login.html"), name='login'),
    path('friends', views.friends, name='friends'),
    path("dm/start/<int:user_id>/", views.start_dm, name="start_dm"),
    path("room/<int:room_id>/", views.talk_room, name="talk_room"),
    path('setting', views.setting, name='setting'),
]
