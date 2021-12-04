from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/foods/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

class Manufacturer(models.Model):
    name = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    domain = models.URLField(blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.name}'

class Food(models.Model):
    name = models.CharField(max_length=30)
    content = MarkdownxField()
    image = models.ImageField(upload_to='foods/images/%Y/%m/%d/', blank=True)
    brand = models.CharField(max_length=20, blank=True)

    price = models.IntegerField()
    calorie = models.IntegerField()
    sales = models.IntegerField(default=0)

    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}] {self.name}'

    def get_absolute_url(self):
        return f'/foods/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return self.food.get_absolute_url()

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/370/78f08c0876b31d05/svg/{self.author.username}/'