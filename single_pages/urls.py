from django.urls import path
from single_pages import views

urlpatterns = [
    path('', views.home), # 홈페이지: 서버IP/
    path('mypage/', views.mypage), # 마이페이지: 서버IP/mypage/
    path('company/', views.company), # 회사소개 페이지: 서버IP/company/
]
