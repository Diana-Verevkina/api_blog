# Generated by Django 3.2.20 on 2023-08-09 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_auto_20230809_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blog_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='news.blog', verbose_name='Блог'),
        ),
    ]
