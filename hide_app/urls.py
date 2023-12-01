from django.urls import path
from . import views

# URLパターンを逆引きできるように名前を付ける
app_name = 'hideapp'

# URLパターンを登録する変数
urlpatterns = [
    # photoアプリへのアクセスはviewsモジュールのIndexViewを実行
    path('', views.RockView.as_view(), name='rock'),
    
    # 写真投稿ページへのアクセスはviewsモジュールのCreatePhotoViewを実行
    path('post/', views.CreatePhotoView.as_view(), name='post'),
    
    # 投稿完了ページへのアクセスはviewsモジュールのPostSuccessViewを実行
    path('post_done/',
         views.PostSuccessView.as_view(),
         name='post_done'),
    
    path('contact/',
         views.ContactView.as_view(),
         name='contact'),
    
]