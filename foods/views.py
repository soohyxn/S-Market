from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from foods.models import Food, Category, Comment, Cart
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages

# 상품 후기(댓글) 등록
def new_comment(request, pk):
    if request.user.is_authenticated: # 로그인을 한 경우
        food = get_object_or_404(Food, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid(): # 정상적으로 폼을 작성한 경우 댓글 등록
                comment = comment_form.save(commit=False)
                comment.food = food
                comment.author = request.user # 후기 작성자를 로그인한 사용자로
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(food.get_absolute_url())
    else:
        raise PermissionDenied

# 상품 후기(댓글) 수정
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm # 수정 페이지 폼

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author: # 로그인한 사용자가 후기 작성자라면 수정 페이지를 보여준다
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return self.request.GET['next'] # 원래 있던 페이지로 이동

# 상품 후기(댓글) 삭제
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user.is_authenticated and request.user == comment.author: # 로그인한 사용자가 후기 작성자라면 후기를 삭제한다
        comment.delete()
        return redirect(request.GET['next']) # 원래 있던 페이지로 이동
    else:
        raise PermissionDenied

# 상품 등록
class FoodCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Food
    fields = ['name', 'content', 'image', 'brand', 'price', 'calorie', 'sales', 'manufacturer', 'category'] # 작성 내용

    def test_func(self): # 상품 등록 페이지에 접근 가능한 사용자를 제한
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser): # 로그인한 사용자가 superuser나 staff라면 상품을 등록할 수 있다
            return super(FoodCreate, self).form_valid(form)
        else:
            return redirect('/food/')

# 상품 수정
class FoodUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Food
    fields = ['name', 'content', 'image', 'brand', 'price', 'calorie', 'sales', 'manufacturer', 'category'] # 작성 내용

    template_name = 'foods/food_update_form.html'

    def test_func(self): # 상품 수정 페이지에 접근 가능한 사용자를 제한
        return self.request.user.is_superuser or self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff): # 로그인한 사용자가 superuser나 staff라면 상품을 수정할 수 있다
            return super(FoodUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError

# 상품 목록
class FoodList(ListView):
    model = Food
    ordering = 'pk' # 상품이 게시된 순으로
    paginate_by = 6 # 한 페이지에 상품 개수

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FoodList, self).get_context_data()
        context['categories'] = Category.objects.all() # 모든 카테고리
        context['food_all_count'] = Food.objects.all().count() # 모든 상품의 개수
        return context

# 상품 상세
class FoodDetail(DetailView):
    model = Food

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FoodDetail, self).get_context_data()
        context['categories'] = Category.objects.all() # 모든 카테고리
        context['comment_form'] = CommentForm # 후기 작성 폼
        return context

# 상품 검색
class FoodSearch(FoodList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q'] # 검색어
        food_list = Food.objects.filter(
            Q(name__contains=q) | Q(content__contains=q) | Q(brand__contains=q)
        ).distinct() # 상품명, 설명, 브랜드명에 검색어가 포함된 상품을 가져온다
        return food_list

    def get_context_data(self, **kwargs):
        context = super(FoodSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'검색결과: {q}' # 검색 결과 정보
        return context

# 상품 카테고리
def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    food_list = Food.objects.filter(category=category) # 카테고리에 속한 상품
    categories = Category.objects.all() # 모든 카테고리

    return render(request, 'foods/food_list.html', {'food_list': food_list, 'category': category, 'categories': categories})

# 상품 찜하기
def like_food(request, pk):
    if request.user.is_authenticated: # 로그인을 한 경우
        food = get_object_or_404(Food, pk=pk)
        if request.user in food.like_users.all(): # 상품의 좋아요한 사용자 목록에 사용자가 있는 경우 목록에서 삭제
            food.like_users.remove(request.user)
        else: # 상품의 좋아요한 사용자 목록에 사용자가 없는 경우 목록에 추가
            food.like_users.add(request.user)
        return redirect(request.GET['next']) # 원래 있던 페이지로 이동
    else:
        raise PermissionDenied

# 장바구니에 상품 추가
def new_cart(request, pk, q):
    if request.user.is_authenticated: # 로그인을 한 경우
        food = get_object_or_404(Food, pk=pk)
        try:
            # 상품이 장바구니에 담겨 있으면 수량 변경
            cart = Cart.objects.get(user=request.user, food=food)
            cart.quantity += q
        except Cart.DoesNotExist:
            # 상품이 장바구니에 없으면 상품 추가
            cart = Cart.objects.create(user=request.user, food=food, quantity=q)
        cart.save()
        messages.success(request, '장바구니에 상품이 담겼습니다.')
        return redirect(food.get_absolute_url())
    else:
        raise PermissionDenied