from django.urls import path
from . import views


app_name='myapp'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('profile_list', views.FriendList.as_view(), name='profile'),
    path('talk_room/<int:pk>/', views.TalkCreate.as_view(), name='detail'),
    path('setting', views.SettingView.as_view(), name='setting'),
    path('update_username',views.UsernameUpdateView.as_view(), name='update_username'),
    path('update_username_complete',views.UsernameUpdateDoneView.as_view(),name="update_username_complete"),
    path('update_email',views.UserEmailUpdateView.as_view(), name='update_email'),
    path('update_email_complete',views.UserEmailUpdateDoneView.as_view(),name="update_email_complete"),
    path('update_image',views.UserImageUpdateView.as_view(), name='update_image'),
    path('update_image_complete',views.UserImageUpdateDoneView.as_view(),name="update_image_complete"),
    path('update_password',views.PasswordChange.as_view(), name='update_password'),
    path('update_password_complete',views.PasswordChangeDone.as_view(),name="update_password_complete"),
]



