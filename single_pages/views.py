from django.shortcuts import render
from foods.models import Food, Category, Cart

categories = Category.objects.all() # 모든 카테고리

# 홈
def home(request):
    recent_foods = Food.objects.order_by('-pk')[:3] # 최신 등록된 상품 3개
    return render(request, 'single_pages/home.html', {'recent_foods': recent_foods, 'categories':  categories})

# 마이페이지
def mypage(request):
    food_list = [] # 찜한 상품 목록

    for food in Food.objects.all():
        if request.user in food.like_users.all():
            food_list.append(food)

    return render(request, 'single_pages/mypage.html', {'categories':  categories, 'food_list': food_list})

# 회사소개
def company(request):
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

# 장바구니
def cart(request):
    cart_list = Cart.objects.filter(user=request.user).order_by('-created_at') # 로그인한 사용자의 장바구니 목록(최신순으로)
    final_price = 0 # 총 상품금액

    for cart in cart_list:
        final_price += cart.food.price * cart.quantity

    return render(request, 'single_pages/cart.html', {'categories':  categories, 'cart_list': cart_list, 'final_price': final_price})