from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name ='kilogram'    # 상단에 app_name을 지정하면 다른 어플리케이션과 충돌하지 않는 네임스페이스가 생성된다.

urlpatterns = [
    # url에 기존방식과 다르게 views.IndexView.as_view()가 사용되었는데, 이는 views 내부로 접근할 때 함수가 아니라 클래스로 접근한다는 뜻이다. 따라서 function_based view가 아니라 generic view로 접근한다.
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    url(r'^upload$', views.upload, name='upload'),
    # url(r'^profile/(?P<pk>[0-9]+)/$', login_required(views.ProfileView.as_view()), name='profile'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.profile, name='profile'),
    url(r'^profile/update/$', login_required(views.ProfileUpdateView.as_view()), name='profile_update'),
]