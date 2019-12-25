from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^task/', views.IdexView.as_view()),
]