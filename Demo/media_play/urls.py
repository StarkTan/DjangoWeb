from django.urls import path

from . import views

app_name = 'media_play'  # 增加命名空间
urlpatterns = [
    path('', views.index, name='index'),
    path('play', views.media_stream, name='media_stream')
]
