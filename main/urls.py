from django.urls import path
from . import views, auth, data_log

urlpatterns = [
    path('', views.main_page, name='home'),
    path('login/', views.login, name='login'),
    path('login_proc/', auth.login_proc, name='login_proc'),
    path('logout/', auth.logout, name='logout'),
    path('logs/', views.logs, name='logs'),
    path('log_proc/', data_log.log_proc, name='log_proc'),
    path('download/', views.download_item, name='download'),
    path('upload/', views.upload_item, name='upload'),
]
