from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):    # 장고에 이 폼이 ModelForm이라는 것을 알려줘야해요. forms.ModelForm은 ModelForm이라는 것을 알려주는 구문이에요.

    class Meta: #  이 구문은 이 폼을 만들기 위해서 어떤 model이 쓰여야 하는지 장고에 알려주는 구문입니다. (model = Post).
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)