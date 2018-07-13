from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('page=<int:page>/', views.index, name='index'),
    path('id=<str:value>/', views.detail, name='detail'),
    path('dir=<str:link>', views.dir_detail, name='dir_detail'),
    path('act=<str:link>', views.act_detail, name='act_detail'),
    path('search/', views.search, name='search'),
]
