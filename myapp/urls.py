from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('friends', views.friends.as_view(), name='friends'),
    path('talk_room/<str:username>', views.talk_room.as_view(), name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username', views.username.as_view(), name='username'),
    path('email', views.email.as_view(), name='email'),
    path('icon', views.icon.as_view(), name='icon'),
    path('password', auth_views.PasswordChangeView.as_view(
        template_name='myapp/password.html',
        success_url=reverse_lazy('password_change_done'),
        ), name='password'),
    path('password/done', auth_views.PasswordChangeDoneView.as_view(
        template_name='myapp/password_change_done.html',
    ), name='password_change_done'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
