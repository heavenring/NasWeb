from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),  # 루트 URL 요청 -> views.home 실행
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('logs/', views.logs, name='logs'),
    path('download/', views.download_item, name='download'),
]
