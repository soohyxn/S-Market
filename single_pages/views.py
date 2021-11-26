from django.shortcuts import render
from foods.models import Food

def home(request):
    recent_foods = Food.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/home.html', {'recent_foods': recent_foods})