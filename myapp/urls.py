from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup_view'),
    path('login/', views.Login.as_view(), name='login_view'),
    path('friends/', views.friends, name='friends'),
    path('talk_room/<int:friend_id>/', views.talk_room, name='talk_room'),
    path('setting/', views.setting, name='setting'),
    path('send_talk/<int:friend_id>/', views.send_talk, name='send_talk'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='myapp/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='myapp/password_change_done.html'), name='password_change_done'),
    path('icon_change/',  views.ChangeIconView.as_view(), name='icon_change'),
    path('icon_change_done/', views.icon_change_done, name='icon_change_done'),
    path('username_change/',  views.ChangeNameView.as_view(), name='username_change'),
    path('username_change_done/', views.username_change_done, name='username_change_done'),
    path('mail_change/',  views.ChangeMailView.as_view(), name='mail_change'),
    path('mail_change_done/', views.mail_change_done, name='mail_change_done'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)