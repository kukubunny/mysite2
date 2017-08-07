from django.db import models
from django.utils import timezone
import random

class GuessNumbers(models.Model):
    name = models.CharField(max_length=24)
    lottos = models.CharField(max_length = 255, default='[1,2,3,4,5,6]')
    text = models.CharField(max_length = 255)
    num_lotto = models.IntegerField(default=5)
    update_date = models.DateTimeField()

    def generate(self):
        self.lottos = ""
        origin = list(range(1,46))
        for _ in range(0, self.num_lotto):
            random.shuffle(origin)
            guess = origin[:6]
            guess.sort()
            self.lottos += str(guess) +'\n'
        self.update_date = timezone.now()
        self.save()

    def __str__(self):
        return "%s %s" % (self.name, self.text)     # 만약 models.py에서 GuessNumbers라는 클래스 안에 위의 코드를 오버라이딩한다면 관리자 페이지에서 출력되는 데이터가 name과 text로 변경된다.
