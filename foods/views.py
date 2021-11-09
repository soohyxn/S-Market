from django.shortcuts import render

def food_list(request):
    return render(request, 'foods/food_list.html')

def food_detail(request):
    return render(request, 'foods/food_detail.html')
