from .models import Comment
from django import forms

# 댓글 등록/수정 폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', ) # 작성 내용