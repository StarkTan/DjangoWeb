from django.urls import path

from . import views

app_name = 'file_upload'  # 增加命名空间
urlpatterns = [
    path('', views.index, name='index'),
    path('form_upload', views.file_upload, name='form_upload'),
    path('ajax_upload', views.file_upload, name='ajax_upload'),
    path('delete', views.file_delete, name='delete'),
]
