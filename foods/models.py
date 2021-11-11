from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

class Food(models.Model):
    name = models.CharField(max_length=30)
    content = MarkdownxField()
    image = models.ImageField(upload_to='foods/images/%Y/%m/%d/', blank=True)
    brand = models.CharField(max_length=20, blank=True)

    price = models.IntegerField()
    calorie = models.IntegerField()
    sales = models.IntegerField(default=0)

    def __str__(self):
        return f'[{self.pk}] {self.name}'

    def get_absolute_url(self):
        return f'/food/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)
