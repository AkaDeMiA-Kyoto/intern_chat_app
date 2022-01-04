from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room', views.talk_room, name='talk_room'),
    path('talk_room/<int:id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('name_alt', views.name_altering, name='name_alt'),
    path('mail_alt', views.mail_altering, name='mail_alt'),
    path('image_alt', views.image_altering, name='image_alt'),
    path('pass_alt', views.pass_altering, name='pass_alt'),
    path('logout', views.logout_view, name='logout_view'),
]
