from django.shortcuts import render
from foods.models import Food, Category

def home(request):
    recent_foods = Food.objects.order_by('-pk')[:3]
    categories = Category.objects.all()
    return render(request, 'single_pages/home.html', {'recent_foods': recent_foods, 'categories':  categories})

def mypage(request):
    categories = Category.objects.all()
    return render(request, 'single_pages/mypage.html', {'categories':  categories})