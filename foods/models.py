from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# 카테고리
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True) # 카테고리명
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self): # 카테고리의 상품을 가져오는 메서드
        return f'/foods/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'

# 제조사
class Manufacturer(models.Model):
    name = models.CharField(max_length=20, unique=True) # 제조사명
    address = models.CharField(max_length=50) # 주소
    contact = models.CharField(max_length=15) # 연락처
    domain = models.URLField(blank=True) # 웹사이트

    def __str__(self):
        return f'[{self.pk}] {self.name}'

# 상품
class Food(models.Model):
    name = models.CharField(max_length=30) # 상품명
    content = MarkdownxField() # 설명
    image = models.ImageField(upload_to='foods/images/%Y/%m/%d/', blank=True) # 이미지
    brand = models.CharField(max_length=20, blank=True) # 브랜드명

    price = models.IntegerField() # 가격
    calorie = models.IntegerField() # 칼로리
    sales = models.IntegerField(default=0) # 판매량

    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.SET_NULL) # 제조사
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL) # 카테고리

    like_users = models.ManyToManyField(User, blank=True) # 상품을 좋아요한 사용자

    def __str__(self):
        return f'[{self.pk}] {self.name}'

    def get_absolute_url(self): # 상품을 가져오는 메서드
        return f'/foods/{self.pk}/'

    def get_content_markdown(self): # 상품 설명을 마크다운으로 가져오는 메서드
        return markdown(self.content)

    def get_like_url(self):
        return f'/foods/like/{self.pk}/'

# 후기(댓글)
class Comment(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE) # 상품
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자
    content = models.TextField() # 후기 내용
    created_at = models.DateTimeField(auto_now_add=True) # 작성날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정날짜

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self): # 후기의 상품을 가져오는 메서드
        return self.food.get_absolute_url()

    def get_avatar_url(self): # 사용자 프로필 이미지를 가져오는 메서드
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return f'https://doitdjango.com/avatar/id/370/78f08c0876b31d05/svg/{self.author.username}/'
