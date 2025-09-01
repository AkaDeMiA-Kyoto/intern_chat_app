from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

app_name = "myapp"
urlpatterns = [
    path('', views.index, name='index'),
    # path('signup', views.signup_view, name='signup_view'),
    path("login/", views.Loginview1.as_view(), name="login"),
    # path('login', views.login_view, name='login_view'),
    # path('friends', views.friends, name='friends'),
    path('talk_room/<int:user_id>/', views.talk_room_view, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('signup/', views.form_signup, name='signup'),
    path('friends/', views.friends_view, name='friends'),
    path('change_username/<int:pk>/',views.Change_username.as_view(),name='username'),
    path('change_email/<int:pk>/',views.Change_email.as_view(),name='email'),
    path('change_icon/<int:pk>/',views.Change_icon.as_view(),name='icon'),
    path('change_password/', views.PasswordChange.as_view(), name='password'),
    path('change_done/', views.PasswordChangeDone.as_view(), name='changedone'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
