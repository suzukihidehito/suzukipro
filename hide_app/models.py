from django.db import models
from account.models import CustomUser

class PhotoPost(models.Model):
    '''投稿されたデータを管理するクラス
    '''
    # CustomUserモデル(のuser_id)とPhotoPostモデルを
    # 1対多の関係で結びつける
    # CustomUserが親でPhotoPostが子の関係となる
    user = models.ForeignKey(
        CustomUser,
        # フィールドのタイトル
        verbose_name='ユーザー',
        # ユーザーを削除する場合はそのユーザーの投稿データもすべて削除する
        on_delete=models.CASCADE
    )
    # タイトル用のフィールド
    title = models.CharField(
        verbose_name='タイトル', # フィールドのタイトル
        max_length=200           # 最大文字数は200     
    )
    # コメント用のフィールド
    comment = models.TextField(
        verbose_name='コメント', # フィールドのタイトル
    )
    # イメージのフィールド1
    image = models.ImageField(
        verbose_name='イメージ', # フィールドのタイトル
        upload_to ='photos'      # MEDIA_ROOT以下のphotosにファイルを保存
    )
    # 投稿日時のフィールド
    posted_at = models.DateTimeField(
        verbose_name='投稿日時', # フィールドのタイトル
        auto_now_add=True        #日時を自動追加
    )
    
    def __str__(self):
        '''オブジェクトを文字列に変換して返す
        
        Returns(str):投稿記事のタイトル
        '''
        return self.title
