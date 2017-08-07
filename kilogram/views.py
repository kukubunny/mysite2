from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required   # 로그인 사람만 upload url 확인 할 수있도록함. 그리고 원하는 메소드 위에 @login_required를 입력해주면 됨.
from django.contrib.auth.models import User

from .forms import UploadForm, ProfileForm, UserForm
from .models import Profile

@login_required
def upload(request):
    if request.method == "POST":
        # save data
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit = False)
            photo.owner = request.user
            form.save()
            return redirect('kilogram:index')

    form = UploadForm()
    return render(request, 'kilogram/upload.html', {'form': form})


class IndexView(ListView):
    # model = Photo
    context_object_name = 'user_photo_list'
    paginate_by = 5 # 페이지당 게시물 개수

    def get_queryset(self):
        user = self.request.user
        return user.photo_set.all().order_by('-pub_date')  # -pub_date에 -는 날짜의 역순을 뜻함

'''
from django.views import generics

class MyListView(generics.ListView):

  model = MyModel
  template_name = 'my_template.html'
  paginated_by = 10
  
  def get_context_data(self, **kwargs): # 또 다른 context가 필요하다 할땐 오버라이드 해주면 된다.
    context = super(MyListView, self).get_context_data(**kwargs)
    context['modelTwo'] = MyModelTwo.objects.all()
    return context
'''

@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    # get 20 public photo only
    photos = user.photo_set.filter(is_public=True)[:20]
    context = {"profile_user": user, "photos": photos}
    return render(request, 'kilogram/profile.html', context)


class ProfileUpdateView(View):
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)

        user_form = UserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

        if hasattr(user, 'profile'):
            profile = user.profile
            profile_form = ProfileForm(initial={
                'nickname': user.profile.nickname,
                'profile_photo': profile.profile_photo,
            })
        else:
            profile_form = ProfileForm()

        return render(request, 'kilogram/profile_update.html',
                      {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        pk = request.user.pk
        u = User.objects.get(id=pk)
        user_form = UserForm(request.POST, instance=u)

        if user_form.is_valid():
            user_form.save()

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        else:
            profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = u
            profile.save()

        return redirect('kilogram:profile', pk)