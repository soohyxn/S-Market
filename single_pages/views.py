from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView

from foods.models import Food, Category, Cart, Order, OrderDetail
from django.contrib import messages

categories = Category.objects.all() # 모든 카테고리

# 홈
def home(request):
    recent_foods = Food.objects.order_by('-pk')[:3] # 최신 등록된 상품 3개
    return render(request, 'single_pages/home.html', {'recent_foods': recent_foods, 'categories':  categories})

# 베스트 상품
def best(request):
    best_foods = Food.objects.order_by('-sales')[:9] # 판매량이 높은 상품 9개
    return render(request, 'single_pages/best.html', {'best_foods': best_foods})

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
        if cart.food.inventory > 0:
            final_price += cart.food.price * cart.quantity

    return render(request, 'single_pages/cart.html', {'categories':  categories, 'cart_list': cart_list, 'final_price': final_price})

# 주문 재고 확인
def check_order(request):
    if request.user.is_authenticated: # 로그인을 한 경우
        cart_list = Cart.objects.filter(user=request.user).order_by('-created_at')
        # 주문 가능한 수량인지 확인
        for cart in cart_list:
            if cart.food.inventory > 0 and cart.quantity > cart.food.inventory:
                messages.info(request, str(cart.food.name) + '의 수량이 재고수량(' + str(cart.food.inventory) + ')를 초과합니다.')
                return redirect('/cart/')
        else:
            return redirect('/order/')
    else:
        raise PermissionDenied

# 주문하기
class Order(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['name', 'address', 'contact']  # 작성 내용
    success_url = '/mypage/'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            order = form.save(commit=False)
            order.user = self.request.user # 주문자를 로그인한 사용자로
            order.save()

            cart_list = Cart.objects.filter(user=self.request.user, food__inventory__gt=0)
            # 장바구니에 담긴 상품을 주문상세에 저장
            for cart in cart_list:
                OrderDetail.objects.create(order=order, food=cart.food, quantity=cart.quantity) # 주문상세 생성
                cart.delete() # 장바구니에서 상품 삭제
                cart.food.inventory -= cart.quantity # 상품 재고량 수정
                cart.food.save()

            return super(Order, self).form_valid(form)
        else:
            return PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(Order, self).get_context_data()
        cart_list = Cart.objects.filter(user=self.request.user, food__inventory__gt=0).order_by('-created_at') # 재고량이 1개 이상인 상품이 담긴 장바구니 목록(최신순으로)
        final_price = 0 # 총 상품금액
        for cart in cart_list:
            final_price += cart.food.price * cart.quantity

        context['cart_list'] = cart_list
        context['final_price'] = final_price
        return context

