from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 루트 URL 요청 -> views.home 실행
]
