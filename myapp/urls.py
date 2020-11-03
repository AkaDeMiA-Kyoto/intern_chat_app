from django.urls import path
from . import views
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.Login.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<friend_username>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_change',views.username_change,name='username_change'),
    path('mail_change',views.mail_change,name='mail_change'),
    path('user_img_change',views.user_img_change,name='user_img_change'),
    


]

urlpatterns += staticfiles_urlpatterns()

