from django import forms    # 장고가 제공해주는 기본 폼인
from .models import GuessNumbers    # 데이터베이스 입력을 위해 추가

class PostForm(forms.ModelForm):
    class Meta:
        model = GuessNumbers
        fields = ('name', 'text',)  # fields는 어떤 필드를 입력받을것인가를 지정하는것