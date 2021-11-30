from django.shortcuts import render
from foods.models import Food, Category

def home(request):
    recent_foods = Food.objects.order_by('-pk')[:3]
    categories = Category.objects.all()
    return render(request, 'single_pages/home.html', {'recent_foods': recent_foods, 'categories':  categories})

def mypage(request):
    categories = Category.objects.all()
    return render(request, 'single_pages/mypage.html', {'categories':  categories})

def company(request):
    categories = Category.objects.all()
    best_foods = Food.objects.all().order_by('-sales')[:5]
    labels1 = []
    data1 = []
    labels2 = []
    data2 = []

    for category in categories:
        labels1.append(category.name)
        data1.append(Food.objects.filter(category=category).count())

    for food in best_foods:
        labels2.append(food.name)
        data2.append(food.sales)

    return render(request, 'single_pages/company.html',
                  {'categories':  categories, 'labels1': labels1, 'data1': data1, 'labels2': labels2, 'data2': data2})