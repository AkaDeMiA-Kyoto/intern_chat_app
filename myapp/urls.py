from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('signup', views.signup_view, name = 'signup_view'),
    path('login', views.login_view, name = 'login_view'),
    path('friends', views.friends, name = 'friends'),
    path('setting', views.setting, name = 'setting'),
    path('accounts/login/', auth_views.LoginView.as_view(), name = 'login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page = 'index'), name = 'logout'),
    path('talk_room/<int:recipient_pk>/', views.talk_room, name = 'talk_room'),
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='myapp/pw_change.html'), name = 'pw_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='myapp/pw_changed.html'), name = 'pw_changed'),
    path('profile/username/', views.username_change_view, name='username_change'),
    path('profile/email/', views.email_change_view, name='email_change'),
    path('profile/icon/', views.icon_change_view, name='icon_change'),
    path('changed', views.changed, name = 'changed')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
