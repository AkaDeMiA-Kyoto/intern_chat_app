from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view, name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:friend_id>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_change', views.username_change, name='username_change'),
    path('username_change_done', views.username_change_done, name='username_change_done'),
    path('email_change', views.email_change, name='email_change'),
    path('email_change_done', views.email_change_done, name='email_change_done'),
    path('icon_change', views.icon_change, name='icon_change'),
    path('icon_change_done', views.icon_change_done, name='icon_change_done'),
    path('password_change', PasswordChangeView.as_view(template_name='myapp/password_change.html'), name='password_change'),
    path('password_change_done', PasswordChangeDoneView.as_view(template_name='myapp/password_change_done.html'), name='password_change_done'),
    path('logout', LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
