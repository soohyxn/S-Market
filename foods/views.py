from django.shortcuts import render
from django.views.generic import ListView, DetailView

from foods.models import Food, Category


class FoodList(ListView):
    model = Food
    ordering = 'pk'

class FoodDetail(DetailView):
    model = Food

def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    food_list = Food.objects.filter(category=category)

    return render(request, 'foods/food_list.html', {'food_list': food_list, 'category': category})