from django.urls import path
from foods import views

urlpatterns = [
    path('', views.FoodList.as_view()), # 상품 전체 페이지: 서버IP/foods/
    path('<int:pk>/', views.FoodDetail.as_view()), # 상품 상세 페이지: 서버IP/foods/{pk}/
    path('<int:pk>/new_comment/', views.new_comment), # 상품 후기 등록: 서버IP/foods/{pk}/new_comment/
    path('category/<str:slug>/', views.category_page), # 상품 카테고리 페이지: 서버IP/foods/category/{slug}/
    path('create_food/', views.FoodCreate.as_view()), # 상품 등록 페이지: 서버IP/foods/create_food/
    path('update_food/<int:pk>/', views.FoodUpdate.as_view()), # 상품 수정 페이지: 서버IP/foods/update_food/{pk}/
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()), # 상품 후기 수정 페이지: 서버IP/foods/update_comment/{pk}/
    path('delete_comment/<int:pk>/', views.delete_comment), # 상품 후기 삭제: 서버IP/foods/delete_comment/{pk}/
    path('search/<str:q>/', views.FoodSearch.as_view()),  # 상품 검색 페이지: 서버IP/foods/search/{q}/
    path('like/<int:pk>/', views.like_food), # 상품 찜하기: 서버IP/foods/like/{pk}/
]
