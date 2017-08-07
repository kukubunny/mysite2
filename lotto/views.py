from django.shortcuts import render, redirect
from lotto.models import GuessNumbers
from .forms import PostForm

def index(request):
    lottos = GuessNumbers.objects.all()
    return render(request, "lotto/default.html", {"lottos": lottos})

def post(request):
    if request.method == "POST":    # request 안에 method 변수 존재, 그 변수가 POST 이거나 GET 일 수 있음
        form = PostForm(request.POST)
        if form.is_valid(): # form에 있는 데이터가 유효하다면
            lotto = form.save(commit = False)       # form.save : db에 필드가 저장
            lotto.generate()
            return redirect('index')
    else:
        form = PostForm()   # POST가 아닐경우 form 출력
        return render(request, "lotto/form.html",{"form": form})

def detail(request, lottokey):
    lotto = GuessNumbers.objects.get(pk = lottokey)
    return render(request, "lotto/detail.html", {"lotto": lotto})