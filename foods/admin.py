from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from foods.models import Food, Manufacturer, Category

admin.site.register(Food, MarkdownxModelAdmin)
admin.site.register(Manufacturer)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)