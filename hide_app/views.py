from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import PhotoPostForm
from .models import PhotoPost
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
# method_decoratorをインポート
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.views.generic import FormView

class RockView(ListView):
    '''トップページのビュー
    '''
    # index.htmlをレンダリングする
    template_name ='rock.html'
    queryset = PhotoPost.objects.order_by('-posted_at')
    # 1ページに表示するレコードの件数
    paginate_by = 3
    
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    '''写真投稿ページのビュー
    
    PhotoPostFormで定義されているモデルとフィールドと連携して
    投稿データをデータベースに登録する
    
    Attributes:
      form_class: モデルとフィールドが登録されたフォームクラス
      template_name: レンダリングするテンプレート
      success_url: データベースへの登録完了後のリダイレクト先
    '''
    # forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class = PhotoPostForm
    # レンダリングするテンプレート
    template_name = "post.html"
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('hideapp:post_done')
    
    def form_valid(self,form):
        '''CreateViewクラスのform_valid()をオーバーライド
        
        フォームのバリデーションを通過したトキに呼ばれる
        フォームデータの登録をここで行う
        
        parameters:
          form(django.forms.Form):
            form_classに格納されているPhotoPostFormオブジェクト
        Return:
          HttpResponseRedirectオブジェクト:
            スーパークラスのform_valid()の戻り値を返すことで、
            success_urlで設定されているURLにリダイレクトされる
        '''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドの格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー
   
    Attributes:
      template_name: レンダリングするテンプレート
    '''
    # index.htmlをレンダリングする
    template_name ='post_success.html'
    
class UserView(ListView):
    '''ユーザーの投稿一覧ページのビュー
    Attributes:
      template_name: レンダリングするテンプレート
      paginate_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name='rock.html'
    # 1ページに表示するレコードの件数
    paginate_by = 3
    
    def get_queryset(self):
        '''クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する
        
        Returns:
          クエリによって取得されたレコード
        '''
        # self.kwargsでキーワードの辞書を取得し、
        # userキーの値(ユーザーテーブルのid)を取得
        user_id = self.kwargs['user']
        # filter(フィールド名=id)で絞り込む
        user_list = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return user_list
      
class ContactView(FormView):
    '''問い合わせページをを表示するビュー
    
        フォームで入力されたデータを取得し、メールの作成と送信を行う
    '''
    # contact.htmlをレンダリングする
    template_name ='contact.html'
    # クラス変数form_classにforms.pyで定義したContactFormを設定
    form_class = ContactForm
    # 送信完了後にリダイレクトするページ
    success_url = reverse_lazy('hideapp:contact')
    
    def form_valid(self, form):
        '''FormViewクラスのform_vaild()をオーバーライド
        
           フォームのバリデーションを通過したデータがPOSTされたときに呼ばれる
           メール送信を行う
           
           parameters:
             form(object):ContactFormのオブジェクト
           Return:
             HttpResponseRedirectのオブジェクト
             オブジェクトをインスタンス化するとsuccess_urlで
             設定されているURLにリダイレクトされる
        '''
        # フォームに入力されたデータをフィールド名を指定して取得
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        # メールのタイトルの書式を設定
        subject = 'お問い合わせ：{}'.format(title)
        # フォームの入力データの書式を設定
        message = \
            '送信者名：{0}\nメールアドレス:{1}\nタイトル:{2}\nメッセージ:{3}'\
            .format(name,email,title,message)
        # メールの送信元のアドレス
        from_email = 'mcd2376085@stu.o-hara.ac.jp'
        # 送信先のメールアドレス
        to_list = ['hiroyuki.fukano@mail.o-hara.ac.jp']
        # EmailMessageオブジェクトを生成
        message = EmailMessage(subject=subject,body=message,from_email=from_email,to=to_list,)
        # EmailMessageクラスのsend()でメールサーバーからメールを送信
        message.send()
        # 送信完了後に表示するメッセージ
        messages.success(self.request,'お問い合わせは正常に送信されました。')
        # 戻り値はスーパークラスのform_vaild()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)