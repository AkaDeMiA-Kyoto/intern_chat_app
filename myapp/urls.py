from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('login', views.login_view.as_view(), name='login'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>/<int:friend_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_change',views.username_change,name='username_change'),
    path('mail_change',views.mail_change,name='mail_change'),
    path('password_change',views.password_change.as_view(),name='password_change'),
    path('logout',views.logout_view.as_view(),name='logout'),
    path('setting2/<int:pk>',views.UserUpdateView.as_view(),name='setting2')
]
