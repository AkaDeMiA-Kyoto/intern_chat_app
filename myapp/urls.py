from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.SignupView.as_view(), name='signup_view'),
    path('login', views.CustomLoginView.as_view(), name='login_view'),
    path('logout',views.CustomLogoutView.as_view(), name='logout_view'),
    path('friends', views.CustomListView.as_view(), name='friends'),
    path('talk_room/<int:friend_id>', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('change_name', views.change_name, name='change_name'),
    path('change_address', views.change_address, name='change_address'),
    path('change_icon',views.change_icon, name='change_icon'),
    path('change_password',views.ChangePassword.as_view(), name='change_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

