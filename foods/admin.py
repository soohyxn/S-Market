from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from foods.models import Food, Manufacturer, Category, Comment, Cart, Order, OrderDetail

admin.site.register(Food, MarkdownxModelAdmin)
admin.site.register(Manufacturer)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderDetail)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)