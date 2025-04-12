from django.urls import path
from . import views, auth

urlpatterns = [
    path('', views.main_page, name='home'),
    path('login/', views.login, name='login'),
    path('login_proc/', auth.login_proc, name='login_proc'),
    path('logout/', auth.logout, name='logout'),
    path('logs/', views.logs, name='logs'),
    path('download/', views.download_item, name='download'),
]
