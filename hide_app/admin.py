from django.contrib import admin
from .models import PhotoPost
    
class PhotoPostAdmin(admin.ModelAdmin):
    '''管理ページのレコード一覧に表示するカラムを設定するクラス
 
    '''
    # レコード一覧にidとtitleを表示
    list_display = ('id', 'title')
    # 表示するカラムにリンクを設定
    list_display_links = ('id', 'title')
# Django管理サイトにPhotoPost、PhotoPostAdminを登録する
admin.site.register(PhotoPost, PhotoPostAdmin)
