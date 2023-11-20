from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view.as_view(), name='login_view'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<int:id>/', views.talk_room, name='talk_room'),
    path('talk_room/<int:id>/send_message/', views.send_message, name='send_message'),
    path('setting/', views.setting, name='setting'),
    path('setting/password/', views.password_change.as_view(), name='password_change'),
    path('setting/done/', views.setting_done.as_view(), name='setting_done'),
    path('setting/logout/', views.logout.as_view(), name='logout'),
    path('setting/email/', views.email_change, name='email_change'),
    path('setting/username/', views.username_change, name='username_change'),
    path('setting/image/', views.image_change, name='image_change'),
]