from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from foods.models import Food, Category
from .forms import CommentForm
from django.shortcuts import get_object_or_404

def new_comment(request, pk):
    if request.user.is_authenticated:
        food = get_object_or_404(Food, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.food = food
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(food.get_absolute_url())
    else:
        raise PermissionDenied

class FoodCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Food
    fields = ['name', 'content', 'image', 'brand', 'price', 'calorie', 'sales', 'manufacturer', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser):
            return super(FoodCreate, self).form_valid(form)
        else:
            return redirect('/food/')

class FoodUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Food
    fields = ['name', 'content', 'image', 'brand', 'price', 'calorie', 'sales', 'manufacturer', 'category']

    template_name = 'foods/food_update_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return super(FoodUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionError


class FoodList(ListView):
    model = Food
    ordering = 'pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FoodList, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context

class FoodDetail(DetailView):
    model = Food

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FoodDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['comment_form'] = CommentForm
        return context

def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    food_list = Food.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request, 'foods/food_list.html', {'food_list': food_list, 'category': category, 'categories': categories})