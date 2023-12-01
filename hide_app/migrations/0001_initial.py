# Generated by Django 4.0 on 2023-11-29 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('comment', models.TextField(verbose_name='コメント')),
                ('image', models.ImageField(upload_to='photos', verbose_name='イメージ')),
                ('posted_at', models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customuser', verbose_name='ユーザー')),
            ],
        ),
    ]