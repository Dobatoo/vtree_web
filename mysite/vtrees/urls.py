from django.urls import path

from . import views

app_name = 'vtrees'
urlpatterns = [
    path('', views.index, name='index'),
    path('video/<str:videos_id>/', views.video, name='video')
]
