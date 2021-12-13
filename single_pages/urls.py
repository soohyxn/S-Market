from django.urls import path
from single_pages import views

urlpatterns = [
    path('', views.home), # 홈페이지: 서버IP/
    path('best/', views.best), # 베스트 상품 페이지: 서버IP/best/
    path('mypage/', views.mypage), # 마이페이지: 서버IP/mypage/
    path('company/', views.company), # 회사소개 페이지: 서버IP/company/
    path('cart/', views.cart), # 장바구니: 서버IP/cart/
]
