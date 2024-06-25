from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('upload_post/', views.upload_post, name='upload_post'),
    path('post_like/', views.post_like, name='post_like'),
    path('follow/', views.follow, name='follow'),
    path('fast_follow/', views.fast_follow, name='fast_follow'),
    path('comment/', views.comment, name='comment'),
    path('explore/', views.explore, name='explore'),
    path('search/', views.search, name='search'),
    path('help/', views.help, name='help'),
    path('like_post/', views.like_post, name='like_post'),
    path('user_messages/', views.user_messages, name='user_messages'),
    path('messages_list/', views.messages_list, name='messages_list'),
    path('load_messages/<int:user_id>/', views.load_messages, name='load_messages'),
    path('send_messages/', views.send_messages, name='send_messages'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]