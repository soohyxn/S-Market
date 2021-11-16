from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/food/category/{self.slug}/'

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
        return f'/food/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)