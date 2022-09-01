from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view.as_view(), name='login'),
    path('logout', views.logout_view.as_view(), name='logout'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:id>', views.talk_room, name='talkroom'),
    path('setting', views.setting, name='setting'),
    path('update', views.update, name='update'),
    path('passwordchange', views.PasswordChangeView.as_view(), name='passwordchange'),
]
