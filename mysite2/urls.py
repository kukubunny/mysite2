from django.conf.urls import include, url
from django.contrib import admin
from lotto import views
from kilogram import views as kilogram_views    # kilogram의 views를 추가해야하는데 다른 어플리케이션과의 충돌을 피하기 위해 as 키워드로 kilogram_views라는 별칭을 만든다.
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^kilogram/', include('kilogram.urls')),   # include 함수를 사용하기 위해서는 반드시 from django.conf.urls import include의 명시가 필요하다.
    url(r'^accounts/', include('allauth.urls')),

    # url(r'^$', login_required(kilogram_views.IndexView.as_view()), name='root'),
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    # url(r'^accounts/signup$', kilogram_views.CreateUserView.as_view(), name='signup'),
    # url(r'^accounts/signup/done$', kilogram_views.RegisteredView.as_view(), name='create_user_done'),

    url(r'^lotto/$', views.index, name='lotto'),
    url(r'^lotto/new$', views.post, name = "new_lotto"),
    url(r'^lotto/(?P<lottokey>[0-9]+)/detail/$', views.detail, name = "lotto_detail"),

    url(r'', include('blog.urls'), name='root'),
    url(r'^blog/$', include('blog.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
auth.urls를 include 할 경우 아래와 같은 url들이 포함됩니다.

^login/$ [name='login']
^logout/$ [name='logout']
^password_change/$ [name='password_change']
^password_change/done/$ [name='password_change_done']
^password_reset/$ [name='password_reset']
^password_reset/done/$ [name='password_reset_done']
^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
^reset/done/$ [name='password_reset_complete']
"""

"""
- 아래와 같이 http://localhost:8000/accounts/ 에서 Allauth가 지원해주는 링크 확인가능

Using the URLconf defined in mysite2.urls, Django tried these URL patterns, in this order:
^admin/
^$ [name='root']
^kilogram/
^accounts/ ^ ^signup/$ [name='account_signup']
^accounts/ ^ ^login/$ [name='account_login']
^accounts/ ^ ^logout/$ [name='account_logout']
^accounts/ ^ ^password/change/$ [name='account_change_password']
^accounts/ ^ ^password/set/$ [name='account_set_password']
^accounts/ ^ ^inactive/$ [name='account_inactive']
^accounts/ ^ ^email/$ [name='account_email']
^accounts/ ^ ^confirm-email/$ [name='account_email_verification_sent']
^accounts/ ^ ^confirm-email/(?P<key>[-:\w]+)/$ [name='account_confirm_email']
^accounts/ ^ ^password/reset/$ [name='account_reset_password']
^accounts/ ^ ^password/reset/done/$ [name='account_reset_password_done']
^accounts/ ^ ^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$ [name='account_reset_password_from_key']
^accounts/ ^ ^password/reset/key/done/$ [name='account_reset_password_from_key_done']
^accounts/ ^social/
^accounts/ ^facebook/
^accounts/ ^facebook/login/token/$ [name='facebook_login_by_token']
^lotto/$ [name='lotto']
^lotto/new$ [name='new_lotto']
^lotto/(?P<lottokey>[0-9]+)/detail/$ [name='lotto_detail']
^files\/(?P<path>.*)$
"""