from django.urls import path
from foods import views

urlpatterns = [
    path('', views.food_list),
    path('detail/', views.food_detail),
]
