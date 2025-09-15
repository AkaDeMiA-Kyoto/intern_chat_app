from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='myapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup_view, name='signup_view'),
    path('login', views.LoginView.as_view(), name='login_view'),
    path('friends', views.friends, name='friends'),
    path('talk_room/<int:pk>/', views.talk_room, name='talk_room'),
    path('setting/<int:pk>', views.setting, name='setting'),
    path('setting_username/<int:pk>', views.UsernameUpdateView.as_view(), name='setting_username'),
    path('setting_email/<int:pk>', views.EmailUpdateView.as_view(), name='setting_email'),
    path('setting_icon/<int:pk>', views.IconUpdateView.as_view(), name='setting_icon'),
    path('setting_password', views.MyPasswordChangeView.as_view(), name='setting_password'),
    path('password_success', views.password_success, name='password_success'),
    path('setting_success/<int:pk>', views.setting_success, name='setting_success'),
    path('logout_view', views.LogoutView.as_view(), name='logout_view')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

