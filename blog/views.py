from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')  # 현재시간보다 작거나 같다는 뜻. (lte : less than equal 로 작거나 같다는 뜻.)
    return render(request, 'blog/post_list.html', {'posts': posts}) # 매개변수 request(사용자가 요청하는 모든 것)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":    # HTML에서 <form>정의에 method="POST"라는 속성이 폼 필드의 값들을 POST로 넘겨 request.POST에 저장되어 조건문으로 POST 구별
        form = PostForm(request.POST)

        if form.is_valid(): # 폼에 들어있는 값들이 올바른지를 확인해야합니다.(모든 필드에는 값이 있어야하고 잘못된 값이 있다면 저장하면 되지 않아야해요) 이를 위해 form.is_valid()을 사용할거에요.
            post = form.save(commit=False)
            # form.save()로 폼을 저장하는 작업과 작성자를 추가하는 작업입니다. (PostForm에는 작성자(author) 필드가 없지만, 필드 값이 필요하죠!)
            # commit=False란 넘겨진 데이터를 바로 Post 모델에 저장하지는 말라는 뜻입니다. 왜냐하면, 작성자를 추가한 다음 저장해야 하니까요.
            # 대부분의 경우에는 commit=False를 쓰지 않고 바로 form.save()를 사용해서 저장해요.
            # 다만 여기서는 작성자 정보를 추가하고 저장해야 하므로 commit=False를 사용하는 거예요. post.save()는 변경사항(작성자 정보를 포함)을 유지할 것이에요.
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)  # 새로 작성한 글을 볼 수 있도록 post_detail 페이지로 이동. pk=post.pk를 사용해 뷰에게 값을 넘겨주고 여기에 post는 새로 생성한 블로그 글.
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

'''
    modelform의 form.is_valid() 메서드는 내부적으로 여러가지 일을 하는데, 
    그 중에 하나는 Model Form의 데이터를 폼 인스턴스로 알아서 저장하는 것이다. 
    이 때 is_valid() 가 True인지 False인지 와는 관계가 없다.
    
    def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        print(post.title) # 1.
        if post_form.is_valid():
            print(post.title) # 2.
            [...]
        else
            print(post.title) # 3.
            [...]


    Post를 수정하는 view이다. 2.와 3.에서 기존의 post의 title 값을 기대하고 작업을 했는데 실제로는 reqeust.POST[‘title’]의 값이 출력된다. 
    1. 에서는 수정하기 전의 title 값을 출력한다. 그 이유는 위에서 언급했듯이 is_valid() 메서드에서 post 인스턴스의 값을 request.POST에 들어있는 값으로 자동으로 설정하기 때문이다.
    
    >>> Post.objects.create(title='origin title', content='content')
    >>> post = Post.objects.get(id=1)
    >>> form = PostForm({'title': 'edited title'}, instance=post)
    >>> post.title
    u'origin title'
    >>> form.is_valid()
    True
    >>> post.title
    u'edited title'
    >>> post2 = Post.objects.get(id=1)  # DB로 부터 새로운 instance를 가져온다
    >>> post2.title                     # DB의 title 값이 그대로이다.
    u'origin title'
    >>> form.save()                     # DB에 form데이터를 저장한다
    >>> post3 = Post.objects.get(id=1)  # 다시 DB로 부터 새로운 instance를 가져온다
    >>> post3.title                     # DB의 title 값이 변경되어있다.
    u'edited title'
    
    is_valid() 를 호출하면 post instance에 form의 값들이 저장되지만 DB에 저장되는 것은 아니다. (post2으로 확인) save()함수를 호출하면 DB에 저장된다. (post3으로 확인)
    
    is_valid() 에서 유효성 검사의 성공 여부와 관계없이 form 데이터가 항상 instance에 저장되는 것을 상기하면서 활용하면 좋을 것 같다. 

'''

@login_required
def post_edit(request, pk): # url로부터 추가로 pk 매개변수를 받아서 처리합니다.
    post = get_object_or_404(Post, pk=pk)
    # get_object_or_404(Post, pk=pk)를 호출하여 수정하고자 하는 글의 Post 모델 인스턴스(instance)로 가져옵니다. (pk로 원하는 글을 찾습니다)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        # 이렇게 가져온 데이터를 폼을 만들 때와(글을 수정할 때 폼에 이전에 입력했던 데이터가 있어야 하겠죠?) 폼을 저장할 때 사용하게 됩니다.

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)

def publish(self):
    self.published_date = timezone.now()
    self.save()

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)