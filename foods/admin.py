from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from foods.models import Food

admin.site.register(Food, MarkdownxModelAdmin)