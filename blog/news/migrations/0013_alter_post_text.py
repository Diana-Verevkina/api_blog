# Generated by Django 3.2.20 on 2023-08-09 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_auto_20230809_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(help_text='Введите текст поста', max_length=140, verbose_name='Текст поста'),
        ),
    ]
