from django.shortcuts import render
from django.views.generic import ListView, DetailView

from foods.models import Food


class FoodList(ListView):
    model = Food
    ordering = '-sales'

class FoodDetail(DetailView):
    model = Food