from django.shortcuts import render
from foods.models import Food, Category

# 홈
def home(request):
    recent_foods = Food.objects.order_by('-pk')[:3] # 최신 등록된 상품 3개
    categories = Category.objects.all() # 모든 카테고리
    return render(request, 'single_pages/home.html', {'recent_foods': recent_foods, 'categories':  categories})

# 마이페이지
def mypage(request):
    categories = Category.objects.all() # 모든 카테고리
    food_list = []
    for food in Food.objects.all():
        if request.user in food.like_users.all():
            food_list.append(food)

    return render(request, 'single_pages/mypage.html', {'categories':  categories, 'food_list': food_list})

# 회사소개
def company(request):
    categories = Category.objects.all() # 모든 카테고리
    best_foods = Food.objects.all().order_by('-sales')[:5] # 판매량이 높은 상품 5개
    labels1 = [] # 카테고리명
    data1 = [] # 각 카테고리의 상품 개수
    labels2 = [] # 상품명
    data2 = [] # 상품 판매량

    # 카테고리별 상품 개수
    for category in categories:
        labels1.append(category.name)
        data1.append(Food.objects.filter(category=category).count())

    # 판매량이 높은 상품 5개
    for food in best_foods:
        labels2.append(food.name)
        data2.append(food.sales)

    return render(request, 'single_pages/company.html',
                  {'categories':  categories, 'labels1': labels1, 'data1': data1, 'labels2': labels2, 'data2': data2})