from django.urls import path
from foods import views

urlpatterns = [
    path('', views.FoodList.as_view()),
    path('<int:pk>/', views.FoodDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('category/<str:slug>/', views.category_page),
    path('create_food/', views.FoodCreate.as_view()),
    path('update_food/<int:pk>/', views.FoodUpdate.as_view()),
]
