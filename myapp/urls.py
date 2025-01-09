from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.form_signup, name='form_signup'),
    path('login/', views.LoginFormView.as_view(), name='LoginFormView'),
    path('friends/', views.friend, name='friends'),
    path('talk_room/<int:user_id>', views.talk_room, name='talk_room'),
    path('logout/', views.LogoutFormView.as_view(), name='logout'),
    path('setting/', views.setting, name='setting'),
    path('namechange/', views.form_namechange, name='namechange'),
    path('mailchange/', views.form_mailchange, name='mailchange'),
    path('imagechange/', views.form_imagechange, name='imagechange'),
    path('passwordchange/', views.PasswordChange.as_view(), name='passwordchange'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)