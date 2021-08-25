from os import name
from django.urls import path

from . import views

app_name = 'vtrees'
urlpatterns = [
    path('', views.index, name='index'),
    path('video/<str:videos_id>/', views.video, name='video'),
    path('channel/<str:channels_id>/', views.channel, name='channel'),
    path('channel/<str:channels_id>/posts', views.channel_posts, name='channel_posts')
    #path('count_register/<str:videos_id>/', views.count_register, name='count_register')
]
