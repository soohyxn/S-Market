from django.urls import path
from foods import views

urlpatterns = [
    path('', views.FoodList.as_view()),
    path('<int:pk>/', views.FoodDetail.as_view()),
    path('category/<str:slug>/', views.category_page),
]
